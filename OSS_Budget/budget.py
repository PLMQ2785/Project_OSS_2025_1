import datetime
from expense import Expense
import matplotlib.pyplot as plt
from collections import defaultdict

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
#---------------------------------------------------#
#<그래프 시각화 추가!>
    def plot_expenses_by_category(self):
        if not self.expenses:
            print("지출 내역이 없어 그래프를 표시할 수 없습니다.\n")
            return

        categories = defaultdict(float)
        for expense in self.expenses:
            categories[expense.category] += expense.amount

        if not categories:
            print("집계할 카테고리 데이터가 없습니다.\n")
            return

        plt.rcParams['font.family'] = 'Malgun Gothic'  # 맑은고딕
        plt.rcParams['axes.unicode_minus'] = False  # 마이너스 폰트 깨짐 방지

        names = list(categories.keys())
        values = list(categories.values())

        plt.figure(figsize=(10, 5)) # 그래프 크기 조절

        # 막대 그래프
        plt.subplot(1, 2, 1)
        bars = plt.bar(names, values)
        plt.xlabel("카테고리")
        plt.ylabel("금액 (원)")
        plt.title("카테고리별 지출 (막대 그래프)")
        plt.xticks(rotation=45, ha="right") # 카테고리 이름이 길 경우를 대비해 회전
        # 막대 위에 금액 표시
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{yval:,.0f}원', va='bottom', ha='center')


        # 원형 차트
        plt.subplot(1, 2, 2)
        plt.pie(values, labels=names, autopct='%1.1f%%', startangle=140)
        plt.title("카테고리별 지출 (원형 차트)")
        plt.axis('equal')  # 원형 차트를 원형으로 만듭니다.

        plt.tight_layout() # 그래프 간 간격 자동 조절
        plt.show()
        print("지출 그래프를 표시했습니다.\n")
#</그래프 시각화 추가!>