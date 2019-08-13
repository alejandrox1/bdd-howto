Feature: Assign a quiz
    Scenario Outline: Teacher assigns quiz to a course
        Given teacher <name>
        When the teacher creates a course in <subject>
        Then the teacher will be able to assign quiz <quiz>

        Examples: courses
        | name | subject | quiz |
        | Mr-m | physics | qm-1 |
        | Mr-m | physics | em-1 |
