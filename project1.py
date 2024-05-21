from abc import ABC, abstractmethod
from collections import defaultdict


# 팩토리 패턴
class BalanceQuestion(ABC):
    @abstractmethod
    def get_question(self):
        pass


class Question1(BalanceQuestion):
    def get_question(self):
        return "성적 C+ 7개(재수강 가능) VS 성적 B0 7개"


class Question2(BalanceQuestion):
    def get_question(self):
        return "학교 70년 다니기 VS 70년대 외대 다니기"


class Question3(BalanceQuestion):
    def get_question(self):
        return "교수님과 70시간 면담 VS 70시간 도서관 공부"


class Question4(BalanceQuestion):
    def get_question(self):
        return "전공 70학점 듣기 VS 교양 70학점 듣기"


class Question5(BalanceQuestion):
    def get_question(self):
        return "시간표 70% 1교시 VS 시간표 70% 9교시"


class Question6(BalanceQuestion):
    def get_question(self):
        return "학식 70번 먹기 VS 70번 연속 굶기"


class QuestionFactory:
    @staticmethod
    def create_question(question_id):
        if question_id == 1:
            return Question1()
        elif question_id == 2:
            return Question2()
        elif question_id == 3:
            return Question3()
        elif question_id == 4:
            return Question4()
        elif question_id == 5:
            return Question5()
        elif question_id == 6:
            return Question6()
        else:
            raise ValueError("Unknown question id")


# 전략패턴
class StudentStrategy(ABC):
    @abstractmethod
    def get_student_info(self):
        pass


class MaleFreshmanStrategy(StudentStrategy):
    def get_student_info(self):
        return "Male", "Freshman"


class MaleSophomoreStrategy(StudentStrategy):
    def get_student_info(self):
        return "Male", "Sophomore"


class MaleJuniorStrategy(StudentStrategy):
    def get_student_info(self):
        return "Male", "Junior"


class MaleSeniorStrategy(StudentStrategy):
    def get_student_info(self):
        return "Male", "Senior"


class FemaleFreshmanStrategy(StudentStrategy):
    def get_student_info(self):
        return "Female", "Freshman"


class FemaleSophomoreStrategy(StudentStrategy):
    def get_student_info(self):
        return "Female", "Sophomore"


class FemaleJuniorStrategy(StudentStrategy):
    def get_student_info(self):
        return "Female", "Junior"


class FemaleSeniorStrategy(StudentStrategy):
    def get_student_info(self):
        return "Female", "Senior"


# 학생 클래스
class Student:
    def __init__(self, strategy: StudentStrategy):
        self.gender, self.grade = strategy.get_student_info()
        self.choices = {}

    def make_choice(self, question_id, choice):
        self.choices[question_id] = choice


class Statistics:
    def __init__(self):
        self.data = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))

    def add_choice(self, student: Student):
        gender = student.gender
        grade = student.grade
        for question_id, choice in student.choices.items():
            self.data[gender][grade][question_id][choice] += 1

    def display_statistics(self):
        for gender in self.data:
            for grade in self.data[gender]:
                print(f"Statistics for {gender}, {grade}:")
                for question_id in self.data[gender][grade]:
                    print(f"  Question {question_id}:")
                    for choice, count in self.data[gender][grade][question_id].items():
                        print(f"    Choice '{choice}': {count}")




# 학생 정보 입력 및 질문 선택
def get_student_choices(student):
    for i in range(1, 7):
        question = QuestionFactory.create_question(i)
        print(question.get_question())
        choice = input(f"Choose for Question {i}: ")
        student.make_choice(i, choice)


# 메인 함수
def main():
    strategies = [MaleFreshmanStrategy(), MaleFreshmanStrategy()]
    students = [Student(strategy) for strategy in strategies]

    for student in students:
        get_student_choices(student)

    stats = Statistics()
    for student in students:
        stats.add_choice(student)

    stats.display_statistics()


if __name__ == "__main__":
    main()
