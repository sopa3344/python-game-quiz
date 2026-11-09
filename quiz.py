"""문제 한 개의 데이터와 동작을 담는 클래스."""


class Quiz:
    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 문자열이어야 합니다.")
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 네 개가 필요합니다.")
        if any(not isinstance(choice, str) or not choice.strip() for choice in choices):
            raise ValueError("선택지에 빈 문자열을 넣을 수 없습니다.")
        # bool도 int의 하위 타입이므로 정확한 int 타입을 확인한다.
        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4의 정수여야 합니다.")
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def display(self):
        print(self.question)
        for number, choice in enumerate(self.choices, start=1):
            print(f"  {number}. {choice}")

    def check_answer(self, answer):
        return self.answer == answer

    def to_dict(self):
        return {"question": self.question, "choices": self.choices[:], "answer": self.answer}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("문제 데이터는 JSON 객체여야 합니다.")
        try:
            return cls(data["question"], data["choices"], data["answer"])
        except KeyError as error:
            raise ValueError("문제 데이터의 필수 항목이 없습니다.") from error
