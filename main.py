"""게임의 시작점. 터미널에서 python main.py로 실행한다."""

from input_helpers import read_number


def main():
    try:
        while True:
            print("\n=== 게임 만드는 사람의 퀴즈 ===")
            print("1. 퀴즈 풀기\n2. 퀴즈 추가\n3. 퀴즈 목록\n4. 점수 확인\n5. 종료")
            selection = read_number("선택: ", 1, 5)
            if selection == 5:
                print("게임을 종료합니다.")
                break
            print("선택한 기능은 다음 단계에서 구현합니다.")
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 게임을 종료합니다.")


if __name__ == "__main__":
    main()
