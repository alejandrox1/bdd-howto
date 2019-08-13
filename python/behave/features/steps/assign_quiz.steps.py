import behave
import src.pkg as pkg


@then("the teacher will be able to assign quiz {quiz}")
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

    assert context.teacher.get_quiz(quiz) == context.course.get_quiz(quiz)
