"""
"""
import src.pkg as pkg


def test_teacher():
    courses = [pkg.Course("physics", None, []), pkg.Course("quantum", None, [])]
    teacher = pkg.Teacher("Mr-m", courses)
    assert teacher.teaches() == courses


def test_create_course():
    teacher = pkg.Teacher("Mr-m")
    teacher.create_course("quantum-mechanics")

    course = pkg.Course("quantum-mechanics", teacher, [])
    assert isinstance(teacher.teaches(), list)
    assert course in teacher.teaches()
