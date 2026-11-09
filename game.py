"""메뉴와 게임 진행을 관리한다."""

from default_quizzes import create_default_quizzes
from input_helpers import read_number


class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None

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

    def run(self):
        while True:
            self.show_menu()
            selection = read_number("선택: ", 1, 5)
            if selection == 1:
                self.play()
            elif selection == 5:
                print("게임을 종료합니다.")
                break
            else:
                print("선택한 기능은 다음 단계에서 구현합니다.")
