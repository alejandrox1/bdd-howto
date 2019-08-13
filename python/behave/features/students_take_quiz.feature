Feature: Students take a quiz
    Scenario Outline: Students submit a quiz assigned to their course
        Given teacher <name>
        When the teacher creates a course in <subject>
        And <students> signup
        And the teacher assigns quiz <quiz>
        Then students will be able to submit their quiz <quiz>


        Examples: courses
        | name | subject | students | quiz |
        | Mr-a | mech    | t1       | s-1 |
        | Mr-a | mech    | t1,t2    | s-2 |
