# 팩토리 패턴, 전략 패턴, 커맨드 패턴 적용됨
import tkinter as tk
from tkinter import ttk

class ChoiceStrategy:
    def make_choice(self, game_instance):
        raise NotImplementedError("make_choice method must be implemented in subclass")

class Option1Strategy(ChoiceStrategy):
    def make_choice(self, game_instance):
        game_instance.responses.append(1)
        game_instance.current_question += 1
        game_instance.display_question()

class Option2Strategy(ChoiceStrategy):
    def make_choice(self, game_instance):
        game_instance.responses.append(2)
        game_instance.current_question += 1
        game_instance.display_question()

class StrategyFactory:
    @staticmethod
    def create_strategy(choice):
        if choice == 1:
            return Option1Strategy()
        elif choice == 2:
            return Option2Strategy()
        else:
            raise ValueError("Invalid choice")

class ChoiceCommand:
    def __init__(self, game_instance, strategy):
        self.game_instance = game_instance
        self.strategy = strategy
    
    def execute(self):
        self.strategy.make_choice(self.game_instance)

class BalanceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("밸런스 게임")
        self.questions = [
            ("성적 C+ 7개(재수강 가능)", "성적 B0 7개"),
            ("학교 70년 다니기", "70년대 외대 다니기"),
            ("교수님과 70시간 면담", "70시간 도서관 공부"),
            ("전공 70학점 듣기", "교양 70학점 듣기"),
            ("시간표 70% 1교시", "시간표 70% 9교시"),
            ("학식 70번 먹기", "70번 연속 굶기")
        ]
        self.responses = []
        self.choice_commands = []
        self.demographics = {
            "1학년": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "2학년": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "3학년": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "4학년": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "남자": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "여자": {"total": 0, "responses": [[] for _ in range(len(self.questions))]}
        }
        self.start_new_session()

    def start_new_session(self):
        self.current_question = 0
        self.responses = []
        self.display_question()

    def display_question(self):
        self.clear_widgets()
        if self.current_question < len(self.questions):
            question = self.questions[self.current_question]
            self.question_label = tk.Label(self.root, text=f"질문 {self.current_question + 1}:", font=("Helvetica", 14))
            self.question_label.pack(pady=20)
            
            strategy_factory = StrategyFactory()
            cmd1 = ChoiceCommand(self, strategy_factory.create_strategy(1))
            cmd2 = ChoiceCommand(self, strategy_factory.create_strategy(2))
            
            self.choice_commands.append(cmd1)
            self.choice_commands.append(cmd2)
            
            self.option1_button = tk.Button(self.root, text=question[0], font=("Helvetica", 12), command=cmd1.execute)
            self.option1_button.pack(side=tk.LEFT, padx=20)
            
            self.option2_button = tk.Button(self.root, text=question[1], font=("Helvetica", 12), command=cmd2.execute)
            self.option2_button.pack(side=tk.RIGHT, padx=20)
        else:
            self.collect_demographics()

    def collect_demographics(self):
        self.clear_widgets()
        self.question_label = tk.Label(self.root, text="학년을 선택하세요:", font=("Helvetica", 14))
        self.question_label.pack(pady=20)
        
        self.grade_var = tk.StringVar(value="1학년")
        grades = ["1학년", "2학년", "3학년", "4학년"]
        for grade in grades:
            tk.Radiobutton(self.root, text=grade, variable=self.grade_var, value=grade).pack(anchor=tk.W)
        
        self.next_button = tk.Button(self.root, text="다음", command=self.collect_gender)
        self.next_button.pack(pady=20)

    def collect_gender(self):
        self.clear_widgets()
        self.question_label = tk.Label(self.root, text="성별을 선택하세요:", font=("Helvetica", 14))
        self.question_label.pack(pady=20)
        
        self.gender_var = tk.StringVar(value="남자")
        genders = ["남자", "여자"]
        for gender in genders:
            tk.Radiobutton(self.root, text=gender, variable=self.gender_var, value=gender).pack(anchor=tk.W)
        
        self.submit_button = tk.Button(self.root, text="제출", command=self.update_statistics)
        self.submit_button.pack(pady=20)

    def update_statistics(self):
        grade = self.grade_var.get()
        gender = self.gender_var.get()
        
        self.demographics[grade]["total"] += 1
        self.demographics[gender]["total"] += 1
        
        for i, response in enumerate(self.responses):
            self.demographics[grade]["responses"][i].append(response)
            self.demographics[gender]["responses"][i].append(response)
        
        self.show_statistics()

    def show_statistics(self):
        self.clear_widgets()
        
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        total_participants = sum([self.demographics[grade]["total"] for grade in ["1학년", "2학년", "3학년", "4학년"]])
        result_text = f"총 참여 인수: {total_participants}\n\n"
        
        for grade in ["1학년", "2학년", "3학년", "4학년"]:
            total = self.demographics[grade]["total"]
            result_text += f"{grade} (총 {total}명):\n"
            for i, responses in enumerate(self.demographics[grade]["responses"]):
                if total > 0:
                    percent1 = (responses.count(1) / total) * 100
                    percent2 = (responses.count(2) / total) * 100
                    result_text += f"질문 {i + 1}: 선택 1 - {percent1:.2f}%, 선택 2 - {percent2:.2f}%\n"
            result_text += "\n"
        
        for gender in ["남자", "여자"]:
            total = self.demographics[gender]["total"]
            result_text += f"{gender} (총 {total}명):\n"
            for i, responses in enumerate(self.demographics[gender]["responses"]):
                if total > 0:
                    percent1 = (responses.count(1) / total) * 100
                    percent2 = (responses.count(2) / total) * 100
                    result_text += f"질문 {i + 1}: 선택 1 - {percent1:.2f}%, 선택 2 - {percent2:.2f}%\n"
            result_text += "\n"

        result_label = tk.Label(scrollable_frame, text=result_text, font=("Helvetica", 12), justify=tk.LEFT)
        result_label.pack(pady=20)
        
        self.new_session_button = tk.Button(scrollable_frame, text="새로운 사용자 시작", command=self.start_new_session)
        self.new_session_button.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = BalanceGame(root)
    root.mainloop()
