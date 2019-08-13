"""                                                                             
"""
import src.pkg as pkg


def test_student():
    courses = [pkg.Course("physics", None, []), pkg.Course("quantum", None, [])]
    student = pkg.Student("bobby", courses)
    assert student.courses_in_progress() == courses


def test_student_signup():
    course = pkg.Course("electrodynamics", None, [])

    student = pkg.Student("R")
    student.signup_for_course(course)

    assert course in student.courses_in_progress()
