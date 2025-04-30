
USE student_performance;

CREATE TABLE Students_Performance (
    StudentID INT PRIMARY KEY,
    Gender ENUM('Male', 'Female', 'O') NOT NULL,
    Age INT NOT NULL CHECK (Age >= 15 AND Age <= 25),
    StudyHoursPerWeek INT NOT NULL CHECK (StudyHoursPerWeek >= 0 AND StudyHoursPerWeek <= 168),
    AttendanceRate DECIMAL(5,2) NOT NULL CHECK (AttendanceRate >= 0 AND AttendanceRate <= 100),
    GPA DECIMAL(3,2) NOT NULL CHECK (GPA >= 0 AND GPA <= 4.0),
    Major VARCHAR(100) NOT NULL,
    PartTimeJob BOOLEAN NOT NULL,
    ExtraCurricularActivities BOOLEAN NOT NULL
);
