"""
"""
import src.pkg as pkg


def test_course():
    """
    A course should be able to hold information about the teacher and the
    students.
    """
    course = pkg.Course("physics", None, [])

    teacher = pkg.Teacher("Mr-m")
    students = [pkg.Student("bobby")]
    course = pkg.Course("physics", teacher, students)
    assert course.get_teacher() == teacher
    assert course.get_students() == students


def test_course_signup():
    """
    A teacher should be able to create a course for which a student can sign
    up.
    """
    teacher = pkg.Teacher("Mr-m")
    student = pkg.Student("bobby")
    course = teacher.create_course("quantum-mechanics")
    student.signup_for_course(course)

    assert teacher.get_name() == course.get_teacher().get_name()
    assert student in course.get_students()
