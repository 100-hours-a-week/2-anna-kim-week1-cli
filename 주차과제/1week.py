import re

# 연산자 우선순위와 결합성 정의
operators = {
    '+': {'precedence': 1, 'associativity': 'L'},
    '-': {'precedence': 1, 'associativity': 'L'},
    '*': {'precedence': 2, 'associativity': 'L'},
    '/': {'precedence': 2, 'associativity': 'L'},
    '%': {'precedence': 2, 'associativity': 'L'},
    '^': {'precedence': 3, 'associativity': 'R'}
}

# 입력받은 숫자와 진법을 기반으로 모든 2, 8, 10, 16진수로 변환하는 함수
def convert_to_all_bases(number_str, input_base):
    try:
        # 입력된 숫자를 주어진 진법으로 정수 변환
        number = int(number_str, input_base)

        # 모든 진법으로 변환 결과 출력
        return {
            "2진수": bin(number),
            "8진수": oct(number),
            "10진수": str(number),
            "16진수": hex(number)
        }
    except ValueError:
        return {"오류": "유효하지 않은 숫자 또는 진법입니다."}

# 1. 입력 받기
def input_expression(use_previous=False, previous_result=None):
    if use_previous and previous_result is not None:
        print(f"이전 결과: {previous_result}")
        expression = input("이전 결과를 포함한 계산식을 입력하세요 (예: + 10): ")
        return f"{previous_result}{expression}"  # 이전 결과와 새 입력을 합침
    else:
        expression = input("새로운 계산식을 입력하세요 (예: 500 + 5 * 10): ")
        return expression

# 2. 토큰화
def tokenize_expression(expression):
    tokens = re.findall(r'\d+|\+|\-|\*|\/|\%|\^|\(|\)', expression)
    return tokens

# 3. 중위 표기법 → 후위 표기법 변환 (Shunting Yard Algorithm)
def infix_to_postfix(tokens):
    output = []  # 후위 표기법 결과 저장
    operator_stack = []  # 연산자 저장 스택

    for token in tokens:
        if token.isdigit():  # 숫자는 바로 출력
            output.append(token)
        elif token in operators:  # 연산자 처리
            while (operator_stack and operator_stack[-1] != '(' and
                   ((operators[token]['associativity'] == 'L' and
                     operators[token]['precedence'] <= operators[operator_stack[-1]]['precedence']) or
                    (operators[token]['associativity'] == 'R' and
                     operators[token]['precedence'] < operators[operator_stack[-1]]['precedence']))):
                output.append(operator_stack.pop())
            operator_stack.append(token)
        elif token == '(':  # 왼쪽 괄호는 스택에 추가
            operator_stack.append(token)
        elif token == ')':  # 오른쪽 괄호는 왼쪽 괄호까지 연산자를 모두 출력
            while operator_stack and operator_stack[-1] != '(':
                output.append(operator_stack.pop())
            operator_stack.pop()  # 왼쪽 괄호 제거

    # 스택에 남아있는 모든 연산자를 출력
    while operator_stack:
        output.append(operator_stack.pop())

    return output

# 4. 후위 표기법 계산
def evaluate_postfix(postfix_tokens):
    stack = []

    for token in postfix_tokens:
        if token.isdigit():  # 숫자는 스택에 추가
            stack.append(int(token))
        elif token in operators:  # 연산자는 스택에서 두 개의 피연산자를 꺼내 계산
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    raise ZeroDivisionError("0으로 나눌 수 없습니다.")
                stack.append(a / b)
            elif token == '%':  # 나머지 연산 추가
                stack.append(a % b)
            elif token == '^':  # 거듭제곱 연산 추가
                stack.append(a ** b)

    return stack[0]  # 최종 결과 반환

# 5. 결과 저장
history = []

def store_in_history(expression, result):
    history.append({"expression": expression, "result": result})

# 6. 결과 출력
def output_result(result):
    print(f"결과: {result}")

# 7. 메인 루프
def main():
    previous_result = None  # 이전 결과를 저장
    while True:
        # 옵션 제공
        print("\n[옵션]")
        print("1. 지난 결과 가져오기")
        print("2. 새로운 계산")
        print("3. 숫자 진법 변환")
        print("4. 프로그램 종료")
        option = input("선택 (1/2/3/4): ").strip()

        if option == "1":
            if previous_result is None:
                print("오류: 이전 계산 결과가 없습니다.")
                continue
            expression = input_expression(use_previous=True, previous_result=previous_result)
        elif option == "2":
            expression = input_expression(use_previous=False)
        elif option == "3":
            try:
                # 진법 입력 및 숫자 입력
                input_base = int(input("입력할 수의 진법을 입력하세요 (2/8/10/16): "))
                if input_base not in [2, 8, 10, 16]:
                    print("오류: 2, 8, 10, 16 중에서 선택하세요.")
                    continue
                number_str = input(f"{input_base}진법으로 표현된 숫자를 입력하세요: ")

                # 진법 변환 결과 출력
                results = convert_to_all_bases(number_str, input_base)
                for base, value in results.items():
                    print(f"{base}: {value}")
            except ValueError:
                print("오류: 올바른 숫자와 진법을 입력하세요.")
            continue  # 진법 변환 이후 다른 계산을 스킵하고 루프 재시작

        elif option == "4":
            print("프로그램을 종료합니다.")
            break
        else:
            print("오류: 잘못된 선택입니다.")
            continue

        # 아래 코드는 "1" 또는 "2" 옵션에서만 실행됨
        # 토큰화
        tokens = tokenize_expression(expression)
        if not tokens:
            print("오류: 유효하지 않은 입력입니다. 다시 시도하세요.")
            continue

        # 중위 표기법 → 후위 표기법 변환
        try:
            postfix = infix_to_postfix(tokens)
        except Exception as e:
            print(f"후위 표기법 변환 중 오류가 발생했습니다: {e}")
            continue

        # 후위 표기법 계산
        try:
            result = evaluate_postfix(postfix)
        except Exception as e:
            print(f"계산 중 오류가 발생했습니다: {e}")
            continue

        # 결과 저장
        store_in_history(expression, result)
        previous_result = result  # 최근 결과 업데이트

        # 결과 출력
        output_result(result)

    # 종료 후 전체 히스토리 출력
    print("\n전체 계산 기록:")
    for record in history:
        print(f"{record['expression']} = {record['result']}")

# 프로그램 실행
if __name__ == "__main__":
    main()
