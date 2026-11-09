"""모든 화면에서 같은 규칙으로 사용자 입력을 받는다."""


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("빈 입력입니다. 내용을 입력해 주세요.")


def read_number(prompt, minimum, maximum):
    while True:
        raw = read_text(prompt)
        try:
            value = int(raw)
        except ValueError:
            print("숫자로 입력해 주세요.")
            continue
        if minimum <= value <= maximum:
            return value
        print(f"{minimum}~{maximum} 사이의 번호를 입력해 주세요.")
