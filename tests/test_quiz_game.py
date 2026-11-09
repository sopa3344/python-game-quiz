"""임시 폴더에서 검증하므로 사용자의 state.json을 바꾸지 않는다."""

import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from default_quizzes import create_default_quizzes
from game import QuizGame, STATE_PATH
from input_helpers import read_number
from main import main
from quiz import Quiz


class QuizGameTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.assertEqual(Path(self.directory.name).resolve().parent, Path(__file__).resolve().parent)
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "state.json"
        self.output = io.StringIO()
        self.redirect = contextlib.redirect_stdout(self.output)
        self.redirect.__enter__()
        self.addCleanup(self.redirect.__exit__, None, None, None)
        self.game = QuizGame(self.path)

    def write_state(self, quizzes=None, score=None):
        data = {"version": 1, "quizzes": quizzes if quizzes is not None else [], "best_score": score}
        self.path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def test_missing_file_uses_six_independent_defaults(self):
        self.assertEqual(len(self.game.quizzes), 6)
        self.assertIsNone(self.game.best_score)
        self.assertIsNot(self.game.quizzes[0], create_default_quizzes()[0])

    def test_quiz_dictionary_roundtrip_and_answers(self):
        quiz = Quiz.from_dict(self.game.quizzes[0].to_dict())
        self.assertTrue(quiz.check_answer(2))
        self.assertFalse(quiz.check_answer(1))

    def test_invalid_quiz_schema_is_rejected(self):
        for item in [None, {}, {"question": " ", "choices": ["a"] * 4, "answer": 1},
                     {"question": "q", "choices": ["a"] * 3, "answer": 1},
                     {"question": "q", "choices": ["a"] * 4, "answer": True},
                     {"question": "q", "choices": ["a", "b", "", "d"], "answer": 1}]:
            with self.subTest(item=item), self.assertRaises(ValueError):
                Quiz.from_dict(item)

    def test_number_input_recovers_from_empty_text_and_range(self):
        with patch("builtins.input", side_effect=["", "  ", "abc", "0", "9", " 2 "]):
            self.assertEqual(read_number("선택: ", 1, 4), 2)
        self.assertIn("빈 입력", self.output.getvalue())
        self.assertIn("숫자로", self.output.getvalue())
        self.assertIn("1~4", self.output.getvalue())

    def test_add_quiz_validates_every_field_and_persists_korean(self):
        values = ["", " 새 문제 ", "", "하나", "둘", "셋", "넷", "abc", "0", "5", " 2 "]
        with patch("builtins.input", side_effect=values):
            self.game.add_quiz()
        restored = QuizGame(self.path)
        self.assertEqual(len(restored.quizzes), 7)
        self.assertEqual(restored.quizzes[-1].question, "새 문제")
        self.assertEqual(restored.quizzes[-1].answer, 2)
        self.assertIn("새 문제", self.path.read_text(encoding="utf-8"))

    def test_all_correct_game_and_restart_score(self):
        with patch("builtins.input", side_effect=["2", "3", "1", "4", "2", "1"]):
            self.game.play()
        self.assertEqual(QuizGame(self.path).best_score, {"correct": 6, "total": 6})
        self.assertIn("100.0점", self.output.getvalue())

    def test_wrong_answers_and_zero_score_are_real_record(self):
        with patch("builtins.input", side_effect=["1", "1", "2", "1", "1", "2"]):
            self.game.play()
        restored = QuizGame(self.path)
        restored.show_score()
        self.assertEqual(restored.best_score, {"correct": 0, "total": 6})
        self.assertIn("오답", self.output.getvalue())
        self.assertIn("최고 점수: 0.0점", self.output.getvalue())

    def test_score_compares_ratio_not_raw_correct_count(self):
        self.game.update_score(4, 5)
        self.game.update_score(5, 10)
        self.assertEqual(self.game.best_score, {"correct": 4, "total": 5})
        self.game.update_score(8, 10)
        self.assertEqual(self.game.best_score, {"correct": 4, "total": 5})
        self.game.update_score(9, 10)
        self.assertEqual(QuizGame(self.path).best_score, {"correct": 9, "total": 10})

    def test_no_previous_game_message(self):
        self.game.show_score()
        self.assertIn("아직 완료한 게임", self.output.getvalue())

    def test_empty_quiz_list_survives_restart(self):
        self.write_state()
        empty = QuizGame(self.path)
        empty.play()
        empty.list_quizzes()
        self.assertEqual(empty.quizzes, [])
        self.assertIn("퀴즈가 없습니다", self.output.getvalue())

    def test_corrupt_json_is_backed_up_then_recovered(self):
        self.path.write_text("{broken", encoding="utf-8")
        recovered = QuizGame(self.path)
        backups = list(self.path.parent.glob("state.corrupt-*.json"))
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_text(encoding="utf-8"), "{broken")
        self.assertTrue(recovered.save_state())
        self.assertEqual(len(QuizGame(self.path).quizzes), 6)

    def test_invalid_utf8_is_recoverable(self):
        self.path.write_bytes(b"\xff\xfe\xff")
        self.assertEqual(len(QuizGame(self.path).quizzes), 6)

    def test_valid_json_with_invalid_schema_recovers(self):
        for data in [[], {}, {"version": 2}, {"version": 1, "quizzes": [7], "best_score": None}]:
            with self.subTest(data=data):
                self.path.write_text(json.dumps(data), encoding="utf-8")
                self.assertEqual(len(QuizGame(self.path).quizzes), 6)

    def test_invalid_score_schema_recovers(self):
        for score in [7, {}, {"correct": True, "total": 1}, {"correct": 2, "total": 1},
                      {"correct": 0, "total": 0}, {"correct": -1, "total": 1}]:
            with self.subTest(score=score):
                self.write_state(score=score)
                self.assertIsNone(QuizGame(self.path).best_score)

    def test_read_failure_does_not_overwrite_unknown_data(self):
        self.game.save_state()
        original = self.path.read_bytes()
        with patch.object(Path, "open", side_effect=PermissionError):
            inaccessible = QuizGame(self.path)
        self.assertFalse(inaccessible.save_state())
        self.assertEqual(self.path.read_bytes(), original)

    def test_backup_failure_preserves_corrupt_original(self):
        self.path.write_text("{broken", encoding="utf-8")
        with patch("game.shutil.copy2", side_effect=PermissionError):
            inaccessible = QuizGame(self.path)
        self.assertFalse(inaccessible.save_state())
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{broken")

    def test_write_failure_is_reported_without_false_success(self):
        with patch("game.tempfile.NamedTemporaryFile", side_effect=PermissionError):
            self.assertFalse(self.game.save_state())
        self.assertIn("저장하지 못했습니다", self.output.getvalue())

    def test_replace_failure_keeps_old_state_and_cleans_temporary_file(self):
        self.game.save_state()
        original = self.path.read_bytes()
        self.game.best_score = {"correct": 1, "total": 1}
        with patch.object(Path, "replace", side_effect=OSError):
            self.assertFalse(self.game.save_state())
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.glob(".quiz-state-*.tmp")), [])

    def test_menu_eof_and_keyboard_interrupt_exit_and_save(self):
        for interruption in [EOFError, KeyboardInterrupt]:
            with self.subTest(interruption=interruption):
                with patch("main.QuizGame", return_value=self.game), patch("builtins.input", side_effect=interruption):
                    main()
                self.assertTrue(self.path.exists())

    def test_interrupted_add_does_not_store_partial_quiz(self):
        with patch("main.QuizGame", return_value=self.game), patch("builtins.input", side_effect=["2", "미완성", KeyboardInterrupt]):
            main()
        self.assertEqual(len(QuizGame(self.path).quizzes), 6)

    def test_interrupted_play_does_not_count_unfinished_score(self):
        with patch("main.QuizGame", return_value=self.game), patch("builtins.input", side_effect=["1", "2", EOFError]):
            main()
        self.assertIsNone(QuizGame(self.path).best_score)

    def test_state_path_is_project_root_not_current_directory(self):
        self.assertEqual(STATE_PATH, Path(__file__).resolve().parents[1] / "state.json")

    def test_real_process_eof_and_persistence_from_other_directory(self):
        # 별도 프로세스를 두 번 띄워 실제 JSON 파일 유지와 EOF 종료를 검증한다.
        project = str(Path(__file__).resolve().parents[1])
        code = ("import sys; sys.path.insert(0, sys.argv[1]); import main; "
                "from game import QuizGame; from pathlib import Path; "
                "main.QuizGame=lambda:QuizGame(Path(sys.argv[2])); main.main()")
        command = [sys.executable, "-X", "utf8", "-c", code, project, str(self.path)]
        first = subprocess.run(command, input="1\n2\n3\n1\n4\n2\n1\n", text=True,
                               encoding="utf-8", capture_output=True, cwd=self.directory.name, timeout=15)
        second = subprocess.run(command, input="4\n5\n", text=True, encoding="utf-8",
                                capture_output=True, cwd=self.directory.name, timeout=15)
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertIn("입력이 중단", first.stdout)
        self.assertIn("최고 점수: 100.0점", second.stdout)
        self.assertNotIn("Traceback", first.stderr + second.stderr)


if __name__ == "__main__":
    unittest.main()
