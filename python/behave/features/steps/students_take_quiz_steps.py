import behave
import src.pkg as pkg


@behave.step("{students} signup")
def step_impl(context, students):
    students = students.split(',')

    context.students = []
    for student in students:
        s = pkg.Student(student)
        s.signup_for_course(context.course)
        context.students.append(s)
    assert len(context.course.get_students()) == len(students)


@behave.step("the teacher assigns quiz {quiz}")
def step_impl(context, quiz):
    context.teacher.create_quiz(quiz, context.course)

    questions = [
        pkg.MultipleChoice([1, 2, 3], 1),
        pkg.MultipleChoice(["a", "b", "c"], "b")
    ]
    for q in questions:
        context.teacher.add_question_to_quiz(quiz, q)

    context.teacher.save_answer_key_for_course(quiz, context.course)
    context.teacher.assign_quiz_to_course(quiz, context.course)

    teachers_question = context.teacher.get_quiz(quiz).list_questions()
    for student in context.students:
        student_questions = student.get_quiz(quiz).list_questions()
        assert set(teachers_question) == set(student_questions)


@behave.then("students will be able to submit their quiz {quiz}")
def step_impl(context, quiz):
    for student in context.students:
        questions = student.get_quiz(quiz).list_questions()

        questions[0].choose_options(1)
        questions[1].choose_options("a")

        student.finished_quiz(quiz)
        quiz_copy = student.get_quiz(quiz)
        assert context.course.look_for_students_quiz(student, quiz) == quiz_copy
