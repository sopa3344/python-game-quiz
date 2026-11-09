"""메뉴와 게임 진행을 관리한다."""

import json
from pathlib import Path
import shutil
import tempfile
from datetime import datetime

from default_quizzes import create_default_quizzes
from input_helpers import read_number, read_text
from quiz import Quiz

STATE_PATH = Path(__file__).resolve().parent / "state.json"


class QuizGame:
    def __init__(self, state_path=STATE_PATH):
        self.state_path = Path(state_path)
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.can_save = True
        self.load_state()

    def load_state(self):
        try:
            with self.state_path.open("r", encoding="utf-8") as file:
                data = json.load(file)
            if not isinstance(data, dict) or data.get("version") != 1:
                raise ValueError("지원하지 않는 저장 형식입니다.")
            if not isinstance(data.get("quizzes"), list) or "best_score" not in data:
                raise ValueError("필수 저장 항목이 없습니다.")
            quizzes = [Quiz.from_dict(item) for item in data["quizzes"]]
            score = data["best_score"]
            if score is not None:
                if not isinstance(score, dict):
                    raise ValueError("점수 형식이 올바르지 않습니다.")
                correct, total = score.get("correct"), score.get("total")
                if type(correct) is not int or type(total) is not int:
                    raise ValueError("정답 수와 문제 수는 정수여야 합니다.")
                if not 0 <= correct <= total or total < 1:
                    raise ValueError("점수의 범위가 올바르지 않습니다.")
            # 전체 검증이 끝나야 현재 데이터를 교체한다.
            self.quizzes, self.best_score = quizzes, score
            print(f"저장된 데이터를 불러왔습니다. 퀴즈 {len(quizzes)}개")
        except FileNotFoundError:
            print("첫 실행입니다. 기본 퀴즈 6개를 준비했습니다.")
        except (ValueError, UnicodeError):
            print("저장 파일이 손상되었습니다. 기본 퀴즈로 시작합니다.")
            backup = self.state_path.with_name(
                f"state.corrupt-{datetime.now():%Y%m%d-%H%M%S-%f}.json"
            )
            try:
                shutil.copy2(self.state_path, backup)
                print(f"손상된 원본을 보관했습니다: {backup.name}")
            except OSError:
                self.can_save = False
                print("원본을 보관할 수 없어 이번 실행에서는 파일을 덮어쓰지 않습니다.")
        except OSError:
            self.can_save = False
            print("저장 파일을 읽지 못했습니다. 기본 퀴즈로 실행하며 원본을 보호합니다.")

    def save_state(self):
        if not self.can_save:
            print("파일 보호 중입니다. 이번 변경은 저장되지 않았습니다.")
            return False
        data = {"version": 1, "quizzes": [quiz.to_dict() for quiz in self.quizzes],
                "best_score": self.best_score}
        temporary_path = None
        try:
            # 완성된 임시 파일로 교체해서 쓰기 실패 시 기존 파일을 지킨다.
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.state_path.parent,
                prefix=".quiz-state-", suffix=".tmp", delete=False
            ) as file:
                temporary_path = Path(file.name)
                json.dump(data, file, ensure_ascii=False, indent=2)
                file.write("\n")
            temporary_path.replace(self.state_path)
            return True
        except OSError:
            print("저장하지 못했습니다. 폴더의 쓰기 권한과 남은 공간을 확인해 주세요.")
            return False
        finally:
            if temporary_path is not None:
                try:
                    temporary_path.unlink(missing_ok=True)
                except OSError:
                    pass

    def show_menu(self):
        print("\n=== 게임 만드는 사람의 퀴즈 ===")
        print("1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 목록\n4. 점수 확인\n5. 종료")

    def play(self):
        if not self.quizzes:
            print("퀴즈가 없습니다. 먼저 퀴즈를 추가해 주세요.")
            return
        correct = 0
        total = len(self.quizzes)
        print(f"\n퀴즈를 시작합니다! 총 {total}문제")
        for number, quiz in enumerate(self.quizzes, start=1):
            print(f"\n[문제 {number}/{total}]")
            quiz.display()
            answer = read_number("정답 번호 (1~4): ", 1, 4)
            if quiz.check_answer(answer):
                correct += 1
                print("정답입니다!")
            else:
                print(f"오답입니다. 정답: {quiz.answer}. {quiz.choices[quiz.answer - 1]}")
        print(f"\n결과: {total}문제 중 {correct}문제 정답! ({correct / total * 100:.1f}점)")

    def add_quiz(self):
        print("\n새로운 퀴즈를 추가합니다.")
        question = read_text("문제: ")
        choices = [read_text(f"선택지 {number}: ") for number in range(1, 5)]
        answer = read_number("정답 번호 (1~4): ", 1, 4)
        # 모든 입력을 마친 뒤에만 추가한다. 중간에 중단된 문제는 남기지 않는다.
        self.quizzes.append(Quiz(question, choices, answer))
        if self.save_state():
            print("퀴즈가 추가되고 저장되었습니다.")
        else:
            print("퀴즈는 메모리에 추가되었습니다. 종료하면 사라질 수 있습니다.")

    def run(self):
        while True:
            self.show_menu()
            selection = read_number("선택: ", 1, 5)
            if selection == 1:
                self.play()
            elif selection == 2:
                self.add_quiz()
            elif selection == 5:
                print("게임을 종료합니다.")
                break
            else:
                print("선택한 기능은 다음 단계에서 구현합니다.")
