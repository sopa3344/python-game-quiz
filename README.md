# 게임 만드는 사람의 퀴즈

Python 기본 문법과 Git을 익히는 콘솔 퀴즈 게임입니다.
주제는 게임 개발 기초입니다. 기획, 개발, 전시를 경험한 학습자가 익숙한 상황으로 코드를 이해할 수 있도록 골랐습니다.

Python 3.10 이상에서 외부 패키지 없이 실행합니다. 실제 검증 환경은 Windows의 Python 3.15.2입니다. WSL2 Ubuntu에서도 같은 소스를 사용할 수 있지만, 이번 실행 환경에서는 WSL 접근이 제한되어 Ubuntu 실행은 검증하지 않았습니다.

이 저장소의 구현과 명령 실행은 학습 보조 도구가 대행했습니다. 학습자가 직접 수행하거나 이해를 검증한 기록과 구분합니다.

## 실행 방법

프로젝트 폴더에서 실행합니다.

```bash
python main.py
```

Ubuntu에서는 `python3 main.py`를 사용합니다. 한국어가 깨지는 Windows 터미널에서는 `python -X utf8 main.py`로 실행합니다. Python이 PATH에 없다면 `py main.py` 또는 설치된 python.exe의 전체 경로를 사용합니다.

```bash
python -m unittest discover -s tests -v
```

위 명령은 사용자 저장 데이터를 건드리지 않고 임시 폴더에서 검사합니다.

## 기능 목록

| 메뉴 | 하는 일 |
| --- | --- |
| 1. 퀴즈 풀기 | 전체 문제 출제, 정답 판정, 결과 표시와 최고 점수 갱신 |
| 2. 퀴즈 추가 | 문제와 선택지 네 개, 정답 번호 입력 후 즉시 저장 |
| 3. 퀴즈 목록 | 등록된 문제 제목과 개수 표시 |
| 4. 점수 확인 | 최고 점수와 당시 정답 수, 전체 문제 수 표시 |
| 5. 종료 | 데이터를 저장하고 종료 |

앞뒤 공백을 제거하고 빈 입력, 문자, 범위 밖 번호를 다시 입력받습니다. Ctrl+C와 EOF가 발생하면 완료한 데이터만 저장하고 종료합니다. 등록 도중 취소한 문제와 끝내지 않은 게임의 점수는 저장하지 않습니다.

기본 문제는 HP, 정수 타입, 프로토타입, 플레이테스트, 파일 저장, Git을 다룹니다. 개발과 전시 현장에서 만나는 상황을 질문으로 만들었습니다.

## 파일 구조

| 경로 | 역할 |
| --- | --- |
| `main.py` | 시작점, Ctrl+C와 EOF 처리, 마지막 저장 |
| `quiz.py` | Quiz 클래스, 문제 출력과 정답 비교 |
| `game.py` | QuizGame 클래스, 메뉴와 플레이, 등록, 점수, 파일 처리 |
| `input_helpers.py` | 빈 문자열과 숫자 입력 검증 |
| `default_quizzes.py` | 기본 퀴즈 여섯 개 생성 |
| `state.json` | 실행하면 프로젝트 루트에 생성되는 개인 데이터 |
| `state.example.json` | 데이터 형식을 읽어 볼 수 있는 예시 |
| `tests/test_quiz_game.py` | 표준 unittest 기반 자동 검증 |
| `docs/learning-guide.md` | 코드 설명과 직접 해 볼 연습 |
| `docs/submission-checklist.md` | 과제 요구사항과 실제 완료 상태 |
| `docs/git-practice.md` | 브랜치와 GitHub 실습 방법 |
| `docs/evidence/` | 실제 실행과 검사 결과 원문 |
| `docs/screenshots/README.md` | 아직 남아 있는 원본 화면 캡처 안내 |

## state.json 설명

경로는 현재 터미널 위치가 아니라 `game.py`가 있는 프로젝트 루트입니다. UTF-8로 저장하며 한국어를 그대로 읽을 수 있습니다. 첫 실행에는 기본 문제를 쓰고, 저장을 완료하면 파일이 생깁니다.

```json
{
  "version": 1,
  "quizzes": [
    {"question": "HP는 보통 무엇인가요?", "choices": ["해상도", "체력", "파일 수", "음량"], "answer": 2}
  ],
  "best_score": {"correct": 1, "total": 1}
}
```

| 필드 | 의미 |
| --- | --- |
| `version` | 저장 형식 버전, 현재 1 |
| `quizzes` | 문제 목록. 비어 있는 목록도 유효함 |
| `question` | 비어 있지 않은 문제 문자열 |
| `choices` | 비어 있지 않은 문자열 네 개 |
| `answer` | 1~4의 정수 정답 번호 |
| `best_score` | 한 번도 완료하지 않았다면 null. 완료했다면 correct와 total |
| `correct`, `total` | 최고 정답률을 기록한 게임의 정답 수와 전체 문제 수 |

점수는 `정답 수 / 전체 문제 수 * 100`입니다. 문제 개수가 달라져도 정답률로 비교합니다. 같은 비율이면 이전 기록을 유지합니다. 0점으로 완료한 게임과 아직 플레이하지 않은 상태는 다릅니다.

손상된 파일은 `state.corrupt-날짜시간.json`으로 보관한 뒤 기본 문제로 복구합니다. 원본을 읽거나 백업하지 못하면 덮어쓰기를 중단합니다. 쓰기 실패는 안내하고 실행을 계속합니다. 완성된 임시 파일로 원본을 교체하며, 파일 교체가 실패하면 이전 데이터가 남습니다. 이 과제는 한 번에 게임 한 개를 실행하는 사용을 전제로 합니다.

`state.json`은 개인 기록이므로 Git에서 제외했습니다. 실행 시 자동 생성되며, 형식 예시는 `state.example.json`으로 공유합니다. 저장 실패 메시지가 나온 경우 재시작 뒤 데이터 유지가 보장되지 않습니다.

## 검증과 제출 상태

자동 테스트 23개를 통과했습니다. 저장과 재시작은 별도 프로세스 실행으로도 확인했습니다. Ctrl+C는 KeyboardInterrupt를 발생시키는 자동 테스트로 검증했으며, 실제 키보드 조작 화면을 촬영한 것은 아닙니다.

로컬 기능별 커밋과 `feature/quiz-play` 병합을 실제로 수행했습니다. GitHub 새 저장소 생성과 업로드, GitHub를 거친 clone과 pull은 아직 완료되지 않았습니다. 터미널의 외부 네트워크 접근 제한과 GitHub 재로그인이 남아 있습니다. 로컬 원격 저장소 실습은 GitHub 완료 증거와 구분합니다.

자세한 기준은 [제출 체크리스트](docs/submission-checklist.md)와 [Git 실습 기록](docs/git-practice.md)을 봅니다.

## 공식 참고 자료

- [Python 클래스](https://docs.python.org/3/tutorial/classes.html)
- [Python JSON](https://docs.python.org/3/library/json.html)
- [Git clone](https://git-scm.com/docs/git-clone)
