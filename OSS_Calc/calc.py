import tkinter as tk
from tkinter import simpledialog, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("계산기")
        self.root.geometry("300x650")  # 크기 살짝 키움 300*400 -> 300*450

        self.expression = ""

        # 입력창
        self.entry = tk.Entry(root, font=("Arial", 24), justify="right")
        self.entry.pack(fill="both", ipadx=8, ipady=15, padx=10, pady=10)

        # 버튼 생성
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', 'C', '+'],
            ['x', 'sin', 'cos', 'tan'],
            ['asin', 'acos', 'atan', 'sqrt'],
            ['exp', 'log', 'log10', 'abs'],
            ['pi', 'e', '(', ')'],
            ['=', 'Plot f(x)']
        ]

        for row in buttons:
            frame = tk.Frame(root)
            frame.pack(expand=True, fill="both")
            for char in row:
                btn = tk.Button(
                    frame,
                    text=char,
                    font=("Arial", 18),
                    command=lambda ch=char: self.on_click(ch)
                )
                # btn.pack(side="left", expand=True, fill="both") #기존코드
                btn.pack(side="left", expand=True, fill="both", padx=1, pady=1)  # 버튼 간격을 조금 더 넓게 조정

    def on_click(self, char):
        if char == 'C':
            self.expression = ""
        elif char == '=':
            try:
                # self.expression = str(eval(self.expression))
                self.expression = self.scientific_calculate(self.expression)
            except Exception:
                self.expression = "에러"
        elif char == 'Plot f(x)':
            # 버튼 누르면
            self.plot_graph()
            return
        elif char == 'pi':
            self.expression += "pi"  # 'pi' 문자열 추가
        elif char == 'e':
            self.expression += "e"  # 'e' 문자열 추가
        elif char == 'x':
            self.expression += "x"  # 'x' 문자열 추가
        else:
            self.expression += str(char)

        self.entry.delete(0, tk.END)
        self.entry.insert(tk.END, self.expression)

    def scientific_calculate(self, expr_to_eval):

        try:
            if not expr_to_eval: # 수식이 없으면?
                return ""

            # 계산에 허용될 명령어 목록들
            allowed_commands = {
                "np": np,
                "sin": np.sin, "cos": np.cos, "tan": np.tan,
                "asin": np.arcsin, "acos": np.arccos, "atan": np.arctan,
                "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
                "exp": np.exp, "log": np.log, "log10": np.log10, "sqrt": np.sqrt,
                "abs": np.abs,
                "pi": np.pi, "e": np.e
            }
            safe_globals = {"__builtins__": None}
            safe_globals.update(allowed_commands)

            result = eval(expr_to_eval, safe_globals, {})
            return str(result)

        except SyntaxError:
            return "구문오류"
        except NameError: # 정의되지 않은 변수나 함수
            return "이름오류"
        except TypeError:
            return "타입오류"
        except ZeroDivisionError:
            return "0으로나눔"
        except Exception: # 그 외 잡다한것들
            return "계산에러"

    def plot_graph(self):
        func_str = self.expression

        if not func_str:
            messagebox.showerror("에러", "수식이 입력되지 않았습니다!")
            return

        try:
            # x 범위 입력 받기
            x_min_str = simpledialog.askstring("입력", "x의 최소값을 입력하세요:", initialvalue="-10")
            if x_min_str is None: return  # 취소
            x_min = float(x_min_str)

            x_max_str = simpledialog.askstring("입력", "x의 최대값을 입력하세요:", initialvalue="10")
            if x_max_str is None: return
            x_max = float(x_max_str)

            num_points_str = simpledialog.askstring("입력", "데이터 포인트 개수:", initialvalue="200")
            if num_points_str is None: return
            num_points = int(num_points_str)

            if x_min >= x_max:
                messagebox.showerror("오류", "x의 최소값은 최대값보다 작아야 합니다.")
                return
            if num_points <= 1:
                messagebox.showerror("오류", "데이터 포인트 개수는 1보다 커야 합니다.")
                return

        except ValueError:
            messagebox.showerror("오류", "숫자 형식으로 올바르게 입력하세요.")
            return

        x_vals = np.linspace(x_min, x_max, num_points)
        y_vals_list = []

        # 사용할 함수 이름들이랑 네임스페이스를 미리 정의해둠!
        # eval함수는 문자열을 그대로 실행하다보니 이상한걸 실행시킬수도 있어서 미리 목록화 시켜둠
        allowed_commands = {
            "np": np,
            "x": None,  # 루프 안에서 할당되므로 초기값은 None으로 줌
            # numpy 수학 함수들
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "asin": np.arcsin, "acos": np.arccos, "atan": np.arctan,
            "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
            "exp": np.exp, "log": np.log, "log10": np.log10, "sqrt": np.sqrt,
            "abs": np.abs, "pi": np.pi, "e": np.e
        }
        # builtins를 None으로 설정하면 빌트인 함수나 모듈 접근을 막아서 이상한 입력 1차 차단
        safe_globals = {"__builtins__": None}
        safe_globals.update(allowed_commands)

        try:
            if 'x' in func_str:
                for x_val in x_vals:
                    safe_globals["x"] = x_val  # 현재 x 값을 네임스페이스(allowed_commands)에 넣기
                    y_vals_list.append(eval(func_str, safe_globals, None))  # 로컬 네임스페이스는 비워둠
            else:
                constant_y_val = eval(func_str, safe_globals, None)
                y_vals_list=[float(constant_y_val)] * num_points

            y_vals_list = np.array(y_vals_list)  # numpy 배열로 변환
        except Exception as e:
            messagebox.showerror("수식 오류", f"수식 계산 중 오류 발생:\n{func_str}\n{e}")
            return

        # 그래프 표시할 새 Toplevel창 생성
        plot_window = tk.Toplevel(self.root)
        plot_window.title(f"그래프: {func_str}")
        plot_window.geometry("600x500")

        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)  # subplot 추가 (1행 1열 1번째)

        ax.plot(x_vals, y_vals_list)
        ax.set_title(f"f(x) = {func_str}")
        ax.set_xlabel("x")
        ax.set_ylabel("f(x)")
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Matplotlib 네비게이션 툴바 추가
        toolbar = NavigationToolbar2Tk(canvas, plot_window)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
