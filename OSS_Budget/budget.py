import datetime
from expense import Expense

import json

class Budget:
    def __init__(self):
        self.expenses = []

    def add_expense(self, category, description, amount):
        today = datetime.date.today().isoformat()
        expense = Expense(today, category, description, amount)
        self.expenses.append(expense)
        print("지출이 추가되었습니다.\n")

    def list_expenses(self):
        if not self.expenses:
            print("지출 내역이 없습니다.\n")
            return
        print("\n[지출 목록]")
        for idx, e in enumerate(self.expenses, 1):
            print(f"{idx}. {e}")
        print()

    def total_spent(self):
        total = sum(e.amount for e in self.expenses)
        print(f"총 지출: {total}원\n")

    def check_list(self):
        if not self.expenses:
            print("저장할 내역이 없습니다.\n")
            return False
        else:
            return True

    def save_to_json(self, filename="budget_data.json"):
        #JSON 파일로 export
        # Expense -> JSON 직렬화
        data_to_save = [vars(expense) for expense in self.expenses]
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, ensure_ascii=False, indent=4)
            print(f"{filename} 데이터가 저장되었습니다.\n")
        except IOError:
            print(f"'{filename}' 저장하는 중 오류가 발생했습니다.\n")

    def load_from_json(self, filename="budget_data.json"):
        #JSON 파일에서 Import
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data_loaded = json.load(f)

            self.expenses = []  # 기존 내역을 지우고 새로 불러온 데이터로 대체
            for item_data in data_loaded:
                # JSON 읽은 딕셔너리에서 Expense 객체 만들기
                expense = Expense(
                    item_data.get('date'),
                    item_data.get('category'),
                    item_data.get('description'),
                    item_data.get('amount')
                )
                self.expenses.append(expense)
            print(f"'{filename}' 파일에서 데이터를 성공적으로 불러왔습니다.\n")
        except FileNotFoundError:
            print(f"'{filename}' 파일을 찾을 수 없습니다.\n")
        except json.JSONDecodeError:
            print(f"'{filename}' 파일을 읽을 수 없습니다.\n")
        except IOError:
            print(f"'{filename}' 파일을 읽는 중 오류가 발생했습니다.\n")