# 팩토리 패턴, 전략 패턴, 커맨드 패턴 적용됨
import tkinter as tk # 파이썬에서 기본적으로 제공하는 GUI 라이브러리 윈도우 창, 버튼, 레이블 등 댜양한 GUI 요소를 만들 수 있게 해줍니다.
from tkinter import ttk # tkinter의 테마가 적용된 위젯을 제공하는 서브 모듈입니다. 'ttk'를 사용하면 좀 더 현대적이고 스타일이 적용된 GUI 요소를 사용할 수 있습니다.

class ChoiceStrategy: # 전략 패턴 추상 클래스 : 게임의 선택 방식을 구현하고, 사용자 입력에 따라 동작을 변경하는 방법을 보여줍니다.
    def make_choice(self, game_instance): # 선택지 구현 메소드
        pass

class Option1_Strategy(ChoiceStrategy): # ChoiceStrategy 상속, 구체 클래스
    def make_choice(self, game_instance):
        game_instance.responses.append(1)  # responses 리스트에 1을 추가한다.
        game_instance.current_question += 1 # 선택지 인덱스 1 증가시킨다.
        game_instance.display_question() # 선택지를 표시한다.

class Option2_Strategy(ChoiceStrategy):
    def make_choice(self, game_instance):
        game_instance.responses.append(2) # responses 리스트에 2를 추가한다.
        game_instance.current_question += 1 # 선택지 인덱스 1 증가시킨다.
        game_instance.display_question() # 선택지를 표시한다.

class StrategyFactory: #팩토리 패턴 : 전략 패턴의 객체 를 생성해준다.
    def create_strategy(self, choice):
        if choice == 1:
            return Option1_Strategy() # 첫번째 선택지를 선택하면 Option1_Strategy 객체 생성
        elif choice == 2:
            return Option2_Strategy() # 두번째 선택지를 선택하면 Option2_Strategy 객체 생성

class ChoiceCommand: # 커맨드 패턴 : 전략패턴의 선택지를 만드는 명령을 객체로 캡슐화 해준다.
    def __init__(self, game_instance, strategy):
        self.game_instance = game_instance 
        self.strategy = strategy
    
    def execute(self): # 캡슐화한 명령을 실행하는 메서드, 실행하면 각 선택지에 대응되는 make_choice 메서드가 실행된다.
        self.strategy.make_choice(self.game_instance) 

class BalanceGame: #밸런스 게임 클래스
    def __init__(self, root):
        self.root = root # 윈도우 생성
        self.root.title("밸런스 게임") # 윈도우 제목
        self.questions = [ # 질문 목록
            ("성적 C+ 7개(재수강 가능)", "성적 B0 7개"),
            ("학교 70년 다니기", "70년대 외대 다니기"),
            ("교수님과 70시간 면담", "70시간 도서관 공부"),
            ("전공 70학점 듣기", "교양 70학점 듣기"),
            ("시간표 70% 1교시", "시간표 70% 9교시"),
            ("학식 70번 먹기", "70번 연속 굶기")
        ]
        self.responses = [] # 사용자 응답을 저장하는 리스트이다.
        self.choice_commands = [] # 커맨드 패턴의 명령 객체를 저장하는 리스트이다.
        self.statics = { # 학년과 성별에 따른 통계를 저장하는 딕셔너리이다.
            "1학년": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "2학년": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "3학년": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "4학년": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "남자": {"total": 0, "responses": [[] for _ in range(len(self.questions))]},
            "여자": {"total": 0, "responses": [[] for _ in range(len(self.questions))]}
        }
        self.start_new_session() # 새로운 세션 시작 메서드

    def start_new_session(self): # 새로운 세션 시작
        self.current_question = 0 # 현재 선택지 인덱스 초기화
        self.responses = [] # 응답 리스트 초기화
        self.display_question() # 선택지 표시 메서드 

    def display_question(self): #선택지 표시 메서드
        #현재 선택지를 표시해준다. 각 선택지는 대응되는 전략을 실행하는 커맨드로 연결된다.
        self.clear_widgets() # 기존 위젯 삭제
        if self.current_question < len(self.questions): # 아직 표시할 선택지가 남았는지 확인
            question = self.questions[self.current_question] # 현재 선택지를 가져옴
            self.question_label = tk.Label(self.root, text=f"질문 {self.current_question + 1}:", font=("Helvetica", 14)) # 선택지 라벨 생성
            self.question_label.pack(pady=20) # 라벨 배치
            
            strategy_factory = StrategyFactory() # 전략 팩토리 객체 생성
            cmd1 = ChoiceCommand(self, strategy_factory.create_strategy(1)) # 각 선택지에 대한 ChoiceCommand 객체를 생성 
            cmd2 = ChoiceCommand(self, strategy_factory.create_strategy(2))
            
            self.choice_commands.append(cmd1) # choice_commands 리스트에 명령 객체를 추가합니다.
            self.choice_commands.append(cmd2) # choice_commands 리스트에 명령 객체를 추가합니다.
            
            self.option1_button = tk.Button(self.root, text=question[0], font=("Helvetica", 12), command=cmd1.execute) # 각 선택지에 대한 버튼 생성 후 윈도우에 배치, 클릭 할 때 커맨드 패턴 execute 됨
            self.option1_button.pack(side=tk.LEFT, padx=20) 
            
            self.option2_button = tk.Button(self.root, text=question[1], font=("Helvetica", 12), command=cmd2.execute)
            self.option2_button.pack(side=tk.RIGHT, padx=20)
        else: # 더 이상 질문이 없으면 collect_grade 메서드 호출
            self.collect_grade()

    def collect_grade(self): # 통계 데이터 
        self.clear_widgets() # 기존 위젯 삭제
        self.question_label = tk.Label(self.root, text="학년을 선택하세요:", font=("Helvetica", 14)) # 학년 선택 라벨 표시
        self.question_label.pack(pady=20)
        
        self.grade_var = tk.StringVar(value="1학년") # 선택된 학년을 저장하는 변수
        grades = ["1학년", "2학년", "3학년", "4학년"]
        for grade in grades: # 각 학년에 대한 라디오 버튼 생성 후 윈도우에 배치
            tk.Radiobutton(self.root, text=grade, variable=self.grade_var, value=grade).pack(anchor=tk.W)
        
        self.next_button = tk.Button(self.root, text="다음", command=self.collect_gender) # 다음 버튼 생성 후 윈도우에 배치
        self.next_button.pack(pady=20)

    def collect_gender(self):
        self.clear_widgets() # 기존 위젯 삭제
        self.question_label = tk.Label(self.root, text="성별을 선택하세요:", font=("Helvetica", 14)) # 성별 선택 라벨 표시
        self.question_label.pack(pady=20)
        
        self.gender_var = tk.StringVar(value="남자") # 선택된 성별을 저장하는 변수
        genders = ["남자", "여자"]
        for gender in genders: # 각 성별에 대한 라디오 버튼을 생성하고 윈도우에 배치
            tk.Radiobutton(self.root, text=gender, variable=self.gender_var, value=gender).pack(anchor=tk.W)
        
        self.submit_button = tk.Button(self.root, text="제출", command=self.update_statistics) # 제출 버튼 생성, 데이터를 제출하고 통계를 업데이트
        self.submit_button.pack(pady=20)

    def update_statistics(self): 
        grade = self.grade_var.get() # 선택된 학년과 성별을 가져옴
        gender = self.gender_var.get()
        
        self.statics[grade]["total"] += 1 # 선택된 학년과 성별의 총 참여자 수를 증가시킵니다.
        self.statics[gender]["total"] += 1
        
        for i, response in enumerate(self.responses): # 각 질문에 대한 응답에 통계에 추가합니다.
            self.statics[grade]["responses"][i].append(response)
            self.statics[gender]["responses"][i].append(response)
        
        self.show_statistics() # 'show_statistics' 메서드를 호출하여 통계를 표시

    def show_statistics(self):
        self.clear_widgets() # 기존 위젯 삭제
        
        canvas = tk.Canvas(self.root) # 통계를 표시할 스크롤 가능한 캔버스와 프레임을 설정
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

        total_participants = sum([self.statics[grade]["total"] for grade in ["1학년", "2학년", "3학년", "4학년"]]) # 총 참여자 수
        result_text = f"총 참여 인수: {total_participants}\n\n" 
        
        for grade in ["1학년", "2학년", "3학년", "4학년"]: # 학년 별 통계 정보를 result_text 에 추가
            total = self.statics[grade]["total"]
            result_text += f"{grade} (총 {total}명):\n"
            for i, responses in enumerate(self.statics[grade]["responses"]): # 각 질문에 대한 선택 비율을 계산하여 result_text에 추가
                if total > 0:
                    percent1 = (responses.count(1) / total) * 100 # 응답 비율 표시
                    percent2 = (responses.count(2) / total) * 100 # 응답 비율 표시
                    question_text = self.questions[i] # 현재 질문을 가져옴
                    result_text += f"{question_text[0]} vs {question_text[1]}:\n 선택 1 - {percent1:.2f}%, 선택 2 - {percent2:.2f}%\n"
            result_text += "\n"
        
        for gender in ["남자", "여자"]: # 성별별 통계 정보를 'result_text'에 추가
            total = self.statics[gender]["total"]
            result_text += f"{gender} (총 {total}명):\n"
            for i, responses in enumerate(self.statics[gender]["responses"]): # 각 질문에 대한 선택 비율을 계산하여 result_text에 추가
                if total > 0:
                    percent1 = (responses.count(1) / total) * 100 # 응답 비율 표시
                    percent2 = (responses.count(2) / total) * 100 # 응답 비율 표시
                    question_text = self.questions[i] # 현재 질문을 가져옴
                    result_text += f"{question_text[0]} vs {question_text[1]}:\n 선택 1 - {percent1:.2f}%, 선택 2 - {percent2:.2f}%\n"
            result_text += "\n"

        result_label = tk.Label(scrollable_frame, text=result_text, font=("Helvetica", 12), justify=tk.LEFT) # 결과 텍스트를 표시하는 라벨을 생성, 스크롤 가능
        result_label.pack(pady=20)
        
        self.new_session_button = tk.Button(scrollable_frame, text="새로운 사용자 시작", command=self.start_new_session) # 새로운 세션을 시작하는 버튼 생성, 스크롤 가능
        self.new_session_button.pack(pady=20)
        
        canvas.pack(side="left", fill="both", expand=True) #캔버스와 스크롤 바 윈도우 배치
        scrollbar.pack(side="right", fill="y")
    
    def clear_widgets(self): # 윈도우에 있는 모든 위젯을 숨김
        for widget in self.root.winfo_children():
            widget.pack_forget()

if __name__ == "__main__": # 메인 Tkinter 윈도우 생성
    root = tk.Tk() 
    app = BalanceGame(root) # balanceGame 클래스 객체화하여 게임 시작
    root.mainloop() #Tkinter 메인 루프를 시작하여 실행