import tkinter as tk
from tkinter import ttk
import abc

class ChoiceStrategy(abc.ABC):
    @abc.abstractmethod
    def handle_choice(self):
        pass

class ChoiceStrategyA(ChoiceStrategy):
    def handle_choice(self):
        # 첫 번째 선택지 처리 로직
        pass

class ChoiceStrategyB(ChoiceStrategy):
    def handle_choice(self):
        # 두 번째 선택지 처리 로직
        pass

class Choice:
    def __init__(self, option1, option2):
        self.option1 = option1
        self.option2 = option2

class ChoiceBuilder:
    def __init__(self):
        self.option1 = None
        self.option2 = None

    def set_option1(self, option1):
        self.option1 = option1
        return self

    def set_option2(self, option2):
        self.option2 = option2
        return self

    def build(self):
        return Choice(self.option1, self.option2)

class DataCollector:
    def __init__(self, choices):
        self.choices = choices
        self.demographics = {
            "1학년": {"total": 0, "responses": [[] for _ in range(len(self.choices))]},
            "2학년": {"total": 0, "responses": [[] for _ in range(len(self.choices))]},
            "3학년": {"total": 0, "responses": [[] for _ in range(len(self.choices))]},
            "4학년": {"total": 0, "responses": [[] for _ in range(len(self.choices))]},
            "남자": {"total": 0, "responses": [[] for _ in range(len(self.choices))]},
            "여자": {"total": 0, "responses": [[] for _ in range(len(self.choices))]}
        }

    def update_statistics(self, grade, gender, responses):
        self.demographics[grade]["total"] += 1
        self.demographics[gender]["total"] += 1
        
        for i, response in enumerate(responses):
            self.demographics[grade]["responses"][i].append(response)
            self.demographics[gender]["responses"][i].append(response)

class BalanceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("밸런스 게임")
        
        self.choices = [
            ChoiceBuilder().set_option1("성적 C+ 7개(재수강 가능)").set_option2("성적 B0 7개").build(),
            ChoiceBuilder().set_option1("학교 70년 다니기").set_option2("70년대 외대 다니기").build(),
            ChoiceBuilder().set_option1("교수님과 70시간 면담").set_option2("70시간 도서관 공부").build(),
            ChoiceBuilder().set_option1("전공 70학점 듣기").set_option2("교양 70학점 듣기").build(),
            ChoiceBuilder().set_option1("시간표 70% 1교시").set_option2("시간표 70% 9교시").build(),
            ChoiceBuilder().set_option1("학식 70번 먹기").set_option2("70번 연속 굶기").build()
        ]
        
        self.responses = []
        self.data_collector = DataCollector(self.choices)
        self.start_new_session()

    def start_new_session(self):
        self.current_question = 0
        self.responses = []
        self.display_question()

    def display_question(self):
        self.clear_widgets()
        
        if self.current_question < len(self.choices):
            choice = self.choices[self.current_question]
            self.question_label = tk.Label(self.root, text=f"질문 {self.current_question + 1}:", font=("Helvetica", 14))
            self.question_label.pack(pady=20)
            
            self.option1_button = tk.Button(self.root, text=choice.option1, font=("Helvetica", 12), command=lambda: self.show_choice(1))
            self.option1_button.pack(side=tk.LEFT, padx=20)
            
            self.option2_button = tk.Button(self.root, text=choice.option2, font=("Helvetica", 12), command=lambda: self.show_choice(2))
            self.option2_button.pack(side=tk.RIGHT, padx=20)
        else:
            self.collect_demographics()

    def show_choice(self, choice):
        self.responses.append(choice)
        self.current_question += 1
        self.display_question()

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
        
        self.data_collector.update_statistics(grade, gender, self.responses)
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

        total_participants = sum([self.data_collector.demographics[grade]["total"] for grade in ["1학년", "2학년", "3학년", "4학년"]])
        result_text = f"총 참여 인수: {total_participants}\n\n"
        
        for grade in ["1학년", "2학년", "3학년", "4학년"]:
            total = self.data_collector.demographics[grade]["total"]
            result_text += f"{grade} (총 {total}명):\n"
            for i, responses in enumerate(self.data_collector.demographics[grade]["responses"]):
                if total > 0:
                    percent1 = (responses.count(1) / total) * 100
                    percent2 = (responses.count(2) / total) * 100
                    result_text += f"질문 {i + 1}: 선택 1 - {percent1:.2f}%, 선택 2 - {percent2:.2f}%\n"
            result_text += "\n"
        
        for gender in ["남자", "여자"]:
            total = self.data_collector.demographics[gender]["total"]
            result_text += f"{gender} (총 {total}명):\n"
            for i, responses in enumerate(self.data_collector.demographics[gender]["responses"]):
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
