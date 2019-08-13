import behave
import src.pkg as pkg


@behave.step("students will be able to submit their quiz {quiz}")
def step_impl(context, quiz):
    print(len(context.students))
    for student in context.students:
        questions = student.get_quiz(quiz).list_questions()

        questions[0].choose_options(1)
        questions[1].choose_options("a")

        student.finished_quiz(quiz)
        quiz_copy = student.get_quiz(quiz)

        assert context.course.look_for_students_quiz(student, quiz) == quiz_copy


@behave.then("teacher will calculate grade for students")
def step_impl(context):
    for student in context.students:
        grades = context.course.grade_student_quizzes(student)
        assert grades == [0.5]
