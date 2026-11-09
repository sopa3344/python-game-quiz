"""게임의 시작점. 터미널에서 python main.py로 실행한다."""

from game import QuizGame


def main():
    try:
        QuizGame().run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")


if __name__ == "__main__":
    main()
