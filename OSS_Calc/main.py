#<라이브러리 pip 설치 시키기>
import subprocess
import sys

def install_Lib():
    try:
        #matplotlib를 설치하는데 실패할수도 있으니까 try로 예외처리 시키기
        subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
        print("matplotlib numpy 설치가 완료되었습니다.")
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
    import numpy
except ImportError:
    #실패하면 이거 실행하기
    install_Lib()

#</라이브러리 pip 설치 시키기>
#이 부분부터 실행되고 나머지 코드 실행되게 위로 옮김


import tkinter as tk
from calc import Calculator


if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()