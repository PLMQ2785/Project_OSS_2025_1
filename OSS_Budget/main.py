#<라이브러리 pip 설치 시키기>
import subprocess
import sys

def install_Lib():
    try:
        #matplotlib를 설치하는데 실패할수도 있으니까 try로 예외처리 시키기
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
        print("matplotlib 설치가 완료되었습니다.")
        input("프로그램을 다시 시작해야 합니다. 계속하려면 Enter를 눌러주세요")
        sys.exit()
    except subprocess.CalledProcessError as e:
        print(f"라이브러리 설치에 실패했습니다: \n{e}\n 관리자 권한이 아니라면 관리자 권한 쉘로 실행해 주세요.")
        sys.exit()
    except FileNotFoundError:
        print("pip를 찾을 수 없습니다.")
        sys.exit()

try:
    #try -> import matplotlib
    #실패했을때 뻗지말고 except실행하게 하기
    import matplotlib
except ImportError:
    #실패하면 이거 실행하기
    install_Lib()

#</라이브러리 pip 설치 시키기>
#이 부분부터 실행되고 나머지 코드 실행되게 위로 옮김


from budget import Budget


def main():
    budget = Budget()

    while True:
        print("==== 간단 가계부 ====")
        print("1. 지출 추가")
        print("2. 지출 목록 보기")
        print("3. 총 지출 보기")
        print("4. 시각화 통계 표시")
        print("5. 종료")
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

        elif choice == "4":
            budget.plot_expenses_by_category()

        elif choice == "5":
            print("가계부를 종료합니다.")
            break

        else:
            print("잘못된 선택입니다.\n")


if __name__ == "__main__":
    main()
