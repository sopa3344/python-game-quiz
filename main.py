"""게임의 시작점. 터미널에서 python main.py로 실행한다."""

from game import QuizGame


def main():
    game = None
    try:
        game = QuizGame()
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되었습니다. 완료한 내용까지만 저장하고 종료합니다.")
    finally:
        if game is not None:
            try:
                if game.save_state():
                    print("데이터를 저장했습니다. 다음에 또 만나요!")
            except KeyboardInterrupt:
                print("\n저장이 중단되었습니다. 마지막으로 저장된 파일을 유지합니다.")


if __name__ == "__main__":
    main()
