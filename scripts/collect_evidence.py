"""실제 프로그램을 별도 폴더에서 실행하고 표준 출력을 보관한다."""

import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from default_quizzes import create_default_quizzes

OUTPUT = ROOT / "docs" / "evidence"
OUTPUT.mkdir(parents=True, exist_ok=True)


def public_text(text):
    """공개 증거에 개인 PC 경로가 들어가지 않도록 치환한다."""
    for path, label in [(Path(sys.executable), "[PYTHON_EXECUTABLE]"),
                        (ROOT, "[PROJECT_ROOT]"), (Path.home(), "[USER_PROFILE]")]:
        text = text.replace(str(path), label).replace(path.as_posix(), label)
    return text


def record(name, command, directory, inputs=None):
    result = subprocess.run(command, cwd=directory, input=inputs, text=True,
                            encoding="utf-8", capture_output=True, timeout=30)
    text = "COMMAND: " + subprocess.list2cmdline(command) + "\n"
    if inputs is not None:
        text += "STDIN (자동 제공):\n" + inputs + "\n"
    text += f"EXIT CODE: {result.returncode}\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    (OUTPUT / name).write_text(public_text(text), encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"{name}: 실행 실패. 저장된 로그를 확인하세요.")


environment = f"Python: {sys.version}\nPlatform: {platform.platform()}\n"
for arguments in [["git", "--version"]]:
    result = subprocess.run(arguments, cwd=ROOT, text=True, encoding="utf-8", capture_output=True, check=True)
    environment += "$ " + " ".join(arguments) + "\n" + result.stdout
environment += "\nWSL 실행은 이번 환경의 접근 제한으로 검증하지 않았습니다.\n"
(OUTPUT / "environment.txt").write_text(environment, encoding="utf-8")

with tempfile.TemporaryDirectory(prefix="quiz-evidence-", dir=OUTPUT) as directory:
    demo = Path(directory)
    assert demo.resolve().parent == OUTPUT.resolve()
    for source in ROOT.glob("*.py"):
        shutil.copy2(source, demo / source.name)
    command = [sys.executable, "-X", "utf8", "main.py"]
    record("menu.txt", command, demo, "\nabc\n9\n 4 \n5\n")
    record("add_quiz.txt", command, demo,
           "2\n게임 전시에서 플레이테스트를 하는 목적은?\n재미와 막히는 구간 확인\n세금 계산\n숙소 예약\n전력 계약\n1\n5\n")
    record("list.txt", command, demo, "3\n5\n")
    record("play.txt", command, demo, "1\n2\n3\n1\n4\n2\n1\n1\n5\n")
    record("score_restart.txt", command, demo, "4\n5\n")
    record("eof.txt", command, demo, "")
    shutil.copy2(demo / "state.json", OUTPUT / "state-after-demo.json")

record("tests.txt", [sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", "tests", "-v"], ROOT)
record("git-log.txt", ["git", "--no-pager", "log", "--oneline", "--graph", "--all"], ROOT)
sample = {"version": 1, "quizzes": [q.to_dict() for q in create_default_quizzes()], "best_score": None}
(ROOT / "state.example.json").write_text(json.dumps(sample, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("실제 출력과 JSON 예시를 docs/evidence에 저장했습니다.")
