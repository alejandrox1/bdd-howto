import copy


class Course(object):

    def __init__(self,
                 name,
                 teacher=None,
                 students=[],
                 quizzes=[],
                 answer_keys=[],
                 student_records=dict()):
        # One teacher per course.
        if teacher is not None:
            Teacher.is_teacher_instance(teacher)

        if students != []:
            for s in students:
                Student.is_student_instance(s)

        if quizzes != []:
            for q in quizzes:
                Quiz.is_quiz_instance(q)

        if answer_keys != []:
            for q in answer_keys:
                Quiz.is_quiz_instance(q)

        self.name = name
        self.teacher = teacher
        self.students = students
        self.quizzes = quizzes
        self.answer_keys = answer_keys
        self.student_records = student_records

    def __repr__(self):
        return "{} with {}".format(self.get_name(), self.get_teacher())

    def __str__(self):
        return "{} with {}".format(self.get_name(), self.get_teacher())

    def __eq__(self, other):
        if self.get_name() != other.get_name():
            return False
        if self.get_teacher() != other.get_teacher():
            return False
        return True

    def __hash__(self):
        _id = "{} with {}".format(self.get_name(), self.teacher())
        return hash(_id)

    @staticmethod
    def is_course_instance(course):
        if not isinstance(course, Course):
            raise ValueError("{} is not a course".format(course))

    def get_name(self):
        return str(self.name)

    def get_teacher(self):
        return self.teacher

    def set_teacher(self, teacher):
        self.teacher = teacher

    def get_students(self):
        return self.students

    def add_student(self, student):
        Student.is_student_instance(student)
        self.students.append(student)

    def assign_quiz(self, quiz):
        # Copy quiz.
        # TODO: could also ceate a deepcopy of the Quiz object and
        # clear the answers.
        quiz_copy = Quiz(quiz.get_name(), quiz.get_course())
        for q in quiz.list_questions():
            quiz_copy.add_question(copy.deepcopy(q))

        self.quizzes.append(quiz_copy)
        for student in self.students:
            student.assign_quiz(quiz_copy)

    def save_answer_key(self, quiz):
        self.answer_keys.append(quiz)

    def get_answer_keys(self):
        return self.answer_keys

    def get_quizzes(self):
        return self.quizzes

    def get_quiz(self, quiz_name):
        for quiz in self.quizzes:
            if quiz.get_name() == quiz_name:
                return quiz
        return None

    def grade_student_quizzes(self, student):
        quizzes = self.student_records[student]
        grades = []
        for quiz in quizzes:
            grades.append(self.grade_quiz(quiz))
        return grades

    def grade_quiz(self, quiz):
        quiz_to_grade = Quiz.copy(quiz)
        answer_key = None

        for answers in self.answer_keys:
            if answers.get_name() == quiz_to_grade.get_name():
                answer_key = answers

        student_answer = quiz_to_grade.list_questions()
        keys = answer_key.list_questions()
        correct_answers = 0
        for k, a in zip(keys, student_answer):
            if k.get_answer() == a.get_answer():
                correct_answers += 1

        return correct_answers / len(keys)

    def add_quiz_to_student(self, quiz, student):
        # Add a quiz to a student's record or instantiate the record for a new
        # student.
        quiz_copy = Quiz.copy(quiz)
        self.student_records.setdefault(student, []).append(quiz_copy)

    def look_for_students_quiz(self, student, quiz_name):
        quizzes = self.student_records[student]
        for quiz in quizzes:
            if quiz.get_name() == quiz_name:
                return quiz
        return None

    def get_student_records(self, student):
        return self.student_records[student]


class Teacher(object):

    def __init__(self, name, courses=[], quizzes=[]):
        if courses != []:
            for c in courses:
                Course.is_course_instance(c)

        if quizzes != []:
            for q in quizzes:
                Quiz.is_quiz_instance(q)

        self.name = name
        self.courses = courses
        self.quizzes = quizzes

    def __repr__(self):
        return "{} teaches {}".format(self.get_name(), self.teaches())

    def __str__(self):
        return "{} teaches {}".format(self.get_name(), self.teaches())

    def __eq__(self, other):
        if self.get_name() != other.get_name():
            return False
        if self.teaches() != other.teaches():
            return False
        return True

    def __hash__(self):
        _id = "{} teaches {}".format(self.get_name(), self.teaches())
        return hash(_id)

    @staticmethod
    def is_teacher_instance(teacher):
        if not isinstance(teacher, Teacher):
            raise ValueError("{} is not a teacher".format(teacher))

    def get_name(self):
        return str(self.name)

    def teaches(self):
        return self.courses

    def create_course(self, course_name):
        new = Course(course_name, self, [])
        self.courses.append(new)
        return new

    def get_quizzes(self):
        return self.quizzes

    def get_quiz(self, quiz_name):
        for quiz in self.quizzes:
            if quiz.get_name() == quiz_name:
                return quiz
        return None

    def create_quiz(self, quiz_name, course):
        quiz = Quiz(quiz_name, course=course)
        self.quizzes.append(quiz)
        return quiz

    def add_question_to_quiz(self, quiz_name, question):
        for quiz in self.quizzes:
            if quiz.get_name() == quiz_name:
                quiz.add_question(question)

    def assign_quiz_to_course(self, quiz_name, course):
        course_to_quiz = None
        quiz_to_assign = None
        for course in self.courses:
            if course == course:
                course_to_quiz = course

        for quiz in self.quizzes:
            if quiz.get_name() == quiz_name:
                # TODO: could also ceate a deepcopy of the Quiz object and
                # clear the answers.
                quiz_to_assign = Quiz(quiz.get_name(), quiz.get_course())
                for q in quiz.list_questions():
                    quiz_to_assign.add_question(copy.deepcopy(q))

        course_to_quiz.assign_quiz(quiz_to_assign)

    def save_answer_key_for_course(self, quiz_name, course):
        course_to_quiz = None
        quiz_to_assign = None
        for course in self.courses:
            if course == course:
                course_to_quiz = course

        for quiz in self.quizzes:
            if quiz.get_name() == quiz_name:
                quiz_to_assign = quiz
                quiz_to_assign = copy.copy(quiz_to_assign)
        course_to_quiz.save_answer_key(quiz_to_assign)


class Student(object):

    def __init__(self, name, courses=[], quizzes=[]):
        if courses != []:
            for c in courses:
                Course.is_course_instance(c)

        if quizzes != []:
            for q in quizzes:
                Quiz.is_quiz_instance(q)

        self.name = name
        self.courses = courses
        self.quizzes = quizzes

    def __repr__(self):
        return "{} in {}".format(self.get_name(), self.courses_in_progress())

    def __str__(self):
        return "{} in {}".format(self.get_name(), self.courses_in_progress())

    def __eq__(self, other):
        if self.get_name() != other.get_name():
            return False
        if self.courses_in_progress() != other.courses_in_progress():
            return False
        return True

    def __hash__(self):
        _id = "{} in {}".format(self.get_name(), self.courses_in_progress())
        return hash(_id)

    @staticmethod
    def is_student_instance(student):
        if not isinstance(student, Student):
            raise ValueError("{} is not a student".format(student))

    def get_name(self):
        return str(self.name)

    def signup_for_course(self, course):
        course.add_student(self)
        self.courses.append(course)
        self.quizzes.extend(course.get_quizzes())

    def courses_in_progress(self):
        return self.courses

    def get_quizzes(self):
        return self.quizzes

    def assign_quiz(self, quiz):
        # TODO: could also ceate a deepcopy of the Quiz object and
        # clear the answers.
        quiz_copy = Quiz(quiz.get_name(), quiz.get_course())
        for q in quiz.list_questions():
            quiz_copy.add_question(copy.deepcopy(q))

        Quiz.is_quiz_instance(quiz_copy)
        self.quizzes.append(quiz_copy)

    def get_quiz(self, quiz_name):
        for quiz in self.quizzes:
            if quiz.get_name() == quiz_name:
                return quiz
        return None

    def finished_quiz(self, quiz_name):
        for quiz in self.quizzes:
            if quiz.get_name() == quiz_name:
                # Mark quiz as done.
                quiz.finish()
                # Submit quiz.
                course = quiz.get_course()
                course.add_quiz_to_student(quiz, self)


class MultipleChoice(object):

    def __init__(self, options, answer=None):
        # We assume that options will be a list of elements.
        self.options = options
        self.answer = answer

    def __repr__(self):
        return "{} in {}".format(self.get_answer(), self.list_options())

    def __str__(self):
        return "{} in {}".format(self.get_answer(), self.list_options())

    def __eq__(self, other):
        if self.get_answer() != other.get_answer():
            return False
        if self.list_options() != other.list_options():
            return False
        return True

    def __hash__(self):
        _id = "{} in {}".format(self.get_answer(), self.list_options())
        return hash(_id)

    @staticmethod
    def is_quiz_instance(multiple_choice):
        if not isinstance(multiple_choice, MultipleChoice):
            raise ValueError(
                "{} is not a MultipleChoice".format(multiple_choice))

    @staticmethod
    def copy(multiple_choice):
        return MultipleChoice(multiple_choice.list_options(),
                              multiple_choice.get_answer())

    def list_options(self):
        return self.options[:]

    def get_answer(self):
        return self.answer

    def choose_options(self, answer):
        self.answer = answer

    def clear_answer(self):
        self.answer = None


class Quiz(object):

    def __init__(self, name, course, questions=None, finished=False):
        if questions is None:
            questions = []

        self.name = name
        self.course = course
        self.questions = questions
        self.finished = finished

    def __repr__(self):
        return "{} in {}".format(self.get_name(), self.list_questions())

    def __str__(self):
        return "{} in {}".format(self.get_name(), self.list_questions())

    def __eq__(self, other):
        if self.list_questions() != other.list_questions():
            return False
        return True

    def __hash__(self):
        _id = "{} in {}".format(self.get_name(), self.list_questions())
        return hash(_id)

    @staticmethod
    def is_quiz_instance(quiz):
        if not isinstance(quiz, Quiz):
            raise ValueError("{} is not a quiz".format(quiz))

    @staticmethod
    def copy(quiz):
        quiz_copy = Quiz(quiz.get_name(), quiz.get_course(), None,
                         quiz.is_finished())
        for q in quiz.list_questions():
            quiz_copy.add_question(MultipleChoice.copy(q))
        return quiz_copy

    def get_name(self):
        return str(self.name)

    def list_questions(self):
        return self.questions

    def add_question(self, question):
        self.questions.append(question)

    def is_finished(self):
        return self.finished

    def finish(self):
        self.finished = True

    def get_course(self):
        return self.course
