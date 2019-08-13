"""
* There are teachers
* There are students
* Students are in classes that teachers teach
* Teachers can create quizzes with multiple questions (these can be multiple choice)
* Teachers can assign quizzes to students
* Students can answer questions; partial quiz submissions can be made
* Quizzes need to be graded
* Teacher can calculate a grade based on quizzes (on a semester basis)
"""
from .main import Course, Teacher, Student, MultipleChoice, Quiz
