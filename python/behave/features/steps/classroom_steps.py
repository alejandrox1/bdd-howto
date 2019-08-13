import behave
import src.pkg as pkg


@behave.given("teacher {name}")
def step_impl(context, name):
    context.teacher = pkg.Teacher(name)


@behave.when("the teacher creates a course in {subject}")
def step_impl(context, subject):
    context.course = context.teacher.create_course(subject)


@behave.then("{students} will be able to sign up")
def step_impl(context, students):
    students = students.split(',')

    context.students = []
    for student in students:
        s = pkg.Student(student)
        s.signup_for_course(context.course)
        context.students.append(s)
    assert len(context.course.get_students()) == len(students)
