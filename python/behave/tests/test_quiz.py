""" c                                                                            
"""
import src.pkg as pkg


def test_multiple_choice():
    question = pkg.MultipleChoice([1, 2, 3])
    question.choose_options(1)

    assert question.get_answer() == 1


def test_quiz():
    """
    One should be able to add questions to a quiz, answer them, and for to have
    questions and answers available.
    """
    course = pkg.Course("physics", None, [])
    quiz = pkg.Quiz("exam-1", course)
    quiz.add_question(pkg.MultipleChoice([1, 2, 3]))
    quiz.add_question(pkg.MultipleChoice(["a", "b", "c"]))

    questions = quiz.list_questions()
    questions[0].choose_options(1)
    questions[1].choose_options("a")

    assert quiz.list_questions()[0].get_answer() == 1
    assert quiz.list_questions()[1].get_answer() == "a"


def test_create_quiz():
    """
    A teacher should be able to create a quiz and add questions to it.
    """
    teacher = pkg.Teacher("Mr-m")
    course = teacher.create_course("quantum-mechanics")
    teacher.create_quiz("quantum-mechanics-quiz", course)

    questions = [
        pkg.MultipleChoice([1, 2, 3]),
        pkg.MultipleChoice(["a", "b", "c"])
    ]
    for q in questions:
        teacher.add_question_to_quiz("quantum-mechanics-quiz", q)

    quiz_questions = teacher.get_quiz("quantum-mechanics-quiz")
    assert set(quiz_questions.list_questions()) == set(questions)


def test_assign_quiz():
    """
    A teacher should be able to create a course, create a quiz with questions,
    and to assign the quiz to students.
    """
    teacher = pkg.Teacher("Mr-m")
    course = teacher.create_course("quantum-mechanics")
    quiz = teacher.create_quiz("quantum-mechanics-quiz", course)

    questions = [
        pkg.MultipleChoice([1, 2, 3]),
        pkg.MultipleChoice(["a", "b", "c"])
    ]
    for q in questions:
        teacher.add_question_to_quiz("quantum-mechanics-quiz", q)

    teacher.assign_quiz_to_course("quantum-mechanics-quiz", course)

    student = pkg.Student("R")
    student.signup_for_course(course)

    teachers_question = teacher.get_quiz(
        "quantum-mechanics-quiz").list_questions()
    students_questions = student.get_quiz(
        "quantum-mechanics-quiz").list_questions()
    assert set(teachers_question) == set(students_questions)


def test_student_quiz():
    """
    A student should be able to answer questions in a quiz and to marked it as
    done (submit it).
    """
    teacher = pkg.Teacher("Mr-m")
    course = teacher.create_course("quantum-mechanics")
    quiz = teacher.create_quiz("quantum-mechanics-quiz", course)

    questions = [
        pkg.MultipleChoice([1, 2, 3]),
        pkg.MultipleChoice(["a", "b", "c"])
    ]
    for q in questions:
        teacher.add_question_to_quiz("quantum-mechanics-quiz", q)

    teacher.assign_quiz_to_course("quantum-mechanics-quiz", course)

    student = pkg.Student("R")
    student.signup_for_course(course)

    questions = student.get_quiz("quantum-mechanics-quiz").list_questions()
    questions[0].choose_options(1)
    questions[1].choose_options("a")
    student.finished_quiz("quantum-mechanics-quiz")

    answered_quiz = course.look_for_students_quiz(student,
                                                  "quantum-mechanics-quiz")
    assert answered_quiz is not None
    assert isinstance(answered_quiz, pkg.Quiz)
    assert answered_quiz.is_finished() == True
    assert answered_quiz.list_questions()[0].get_answer() == 1
    assert answered_quiz.list_questions()[1].get_answer() == "a"


def test_grade_student_quiz():
    """                                                                         
    A student should be able to answer a quiz, submit it, and have it graded. 
    """
    teacher = pkg.Teacher("Mr-n")
    course = teacher.create_course("qm")
    quiz = teacher.create_quiz("qm-quiz", course)

    questions = [
        pkg.MultipleChoice([1, 2, 3], 1),
        pkg.MultipleChoice(["a", "b", "c"], "b")
    ]
    for q in questions:
        teacher.add_question_to_quiz("qm-quiz", q)

    teacher.save_answer_key_for_course("qm-quiz", course)
    teacher.assign_quiz_to_course("qm-quiz", course)

    student = pkg.Student("R")
    student.signup_for_course(course)

    questions = student.get_quiz("qm-quiz").list_questions()
    questions[0].choose_options(1)
    print("1. ", course.get_answer_keys())
    questions[1].choose_options("a")
    print("1. ", course.get_answer_keys())
    student.finished_quiz("qm-quiz")

    grades = course.grade_student_quizzes(student)
    assert grades == [0.5]
