Feature: Create a course
    Scenario Outline: Create a course
        Given teacher <name>
        When the teacher creates a course in <subject>
        Then <students> will be able to sign up
        
        Examples: courses
        | name | subject | students |
        | Mr-m | physics | s1       |
        | Mr-m | physics | s1,s2    |
