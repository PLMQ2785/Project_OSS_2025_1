from budget import Budget


def main():
    budget = Budget()
    default_json_filename = "budget_data.json"

    while True:
        print("==== 간단 가계부 ====")
        print("1. 지출 추가")
        print("2. 지출 목록 보기")
        print("3. 총 지출 보기")
        print("4. JSON 내보내기")
        print("5. JSON 불러오기")
        print("6. 종료")
        choice = input("선택 > ")

        if choice == "1":
            category = input("카테고리 (예: 식비, 교통 등): ")
            description = input("설명: ")
            try:
                amount = int(input("금액(원): "))
            except ValueError:
                print("잘못된 금액입니다.\n")
                continue
            budget.add_expense(category, description, amount)

        elif choice == "2":
            budget.list_expenses()

        elif choice == "3":
            budget.total_spent()

        elif choice == "4": # JSON으로 저장
            if budget.check_list():
                filename = input(f"저장할 JSON 파일 이름 입력 (기본값: {default_json_filename}): ")
                if not filename: # 입력하지 않으면 기본값 사용
                    filename = default_json_filename
                budget.save_to_json(filename)

        elif choice == "5": # JSON에서 불러오기
            filename = input(f"불러올 JSON 파일 이름 입력 (기본값: {default_json_filename}): ")
            if not filename: # 입력하지 않으면 기본값 사용
                filename = default_json_filename
            budget.load_from_json(filename)

        elif choice == "6":
            print("가계부를 종료합니다.")
            break

        else:
            print("잘못된 선택입니다.\n")


if __name__ == "__main__":
    main()
