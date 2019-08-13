Feature: Teacher grades course
    Scenario Outline: Teacher grades all quizzes taken by students
        Given teacher <name>
        When the teacher creates a course in <subject>
        And <students> signup
        And the teacher assigns quiz <quiz>
        And students will be able to submit their quiz <quiz>
        Then teacher will calculate grade for students


        Examples: courses
        | name | subject | students | quiz |
        | Mr-n | math    | s        | st-1 |
