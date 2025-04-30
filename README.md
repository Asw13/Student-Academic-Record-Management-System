# Student Academic Performance Management System

A Flask-based web application to manage and analyze student academic performance data. The system allows users to enter student records, import data from CSV files, and visualize performance metrics such as GPA distribution and attendance vs. GPA correlations. It uses a MySQL database to store data and provides a user-friendly interface with Tailwind CSS styling and Chart.js for visualizations.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [Dataset](#dataset)
- [Setup](#setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Importing CSV Data](#importing-csv-data)
- [Visualizations](#visualizations)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Data Entry**: Add student records via a web form with validation for fields like GPA, Age, and Attendance Rate.
- **Data Viewing**: Display student records in a tabular format.
- **CSV Import**: Import student data from CSV files with validation to ensure compliance with database constraints.
- **Visualizations**:
  - GPA Distribution (histogram).
  - Attendance vs. GPA (scatter plot).
- **API Endpoint**: Retrieve student data in JSON format (`/api/students`).
- **Database Integrity**: Enforce constraints (e.g., `GPA` between 0 and 4.0, `Age` between 15 and 25).
- **Responsive Design**: Built with Tailwind CSS for a modern, mobile-friendly interface.

## Technologies
- **Backend**: Flask (Python)
- **Database**: MySQL
- **Frontend**: HTML, Tailwind CSS, Chart.js (for visualizations)
- **Data Processing**: Pandas (for CSV validation)
- **Dependencies**:
  - `flask`
  - `mysql-connector-python`
  - `pandas`

## Dataset
The system uses a synthetic dataset designed to simulate student academic performance. The dataset includes the following columns:

| Column                     | Description                                          | Constraints                              |
|----------------------------|-----------------------------------------------------|------------------------------------------|
| `StudentID`                | Unique identifier for each student                  | Integer, Primary Key                     |
| `Gender`                   | Student gender                                      | ENUM('M', 'F', 'O')                      |
| `Age`                      | Student age                                         | Integer, 15-25                           |
| `StudyHoursPerWeek`        | Hours spent studying per week                      | Integer, 0-168                           |
| `AttendanceRate`           | Percentage of classes attended                     | Decimal(5,2), 0-100                      |
| `GPA`                      | Grade Point Average                                | Decimal(3,2), 0-4.0                      |
| `Major`                    | Student's field of study                           | Varchar(100), Non-empty                  |
| `PartTimeJob`              | Whether the student has a part-time job            | Boolean (0/1)                            |
| `ExtraCurricularActivities`| Whether the student participates in activities      | Boolean (0/1)                            |

**Note**: This dataset is synthetic and intended for educational purposes only, as per the dataset disclaimer.

## Setup

### Prerequisites
- Python 3.8+
- MySQL Server
- Git (optional, for cloning the repository)

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/student-performance-management.git
   cd student-performance-management
   ```

2. **Install Dependencies**:
   Create a virtual environment and install the required packages:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install flask mysql-connector-python pandas
   ```

3. **Set Up MySQL Database**:
   - Create the database and table by running the SQL script (`schema.sql`):
     ```sql
     CREATE DATABASE student_performance;
     USE student_performance;

     CREATE TABLE Students_Performance (
         StudentID INT PRIMARY KEY,
         Gender ENUM('M', 'F', 'O') NOT NULL,
         Age INT NOT NULL CHECK (Age >= 15 AND Age <= 25),
         StudyHoursPerWeek INT NOT NULL CHECK (StudyHoursPerWeek >= 0 AND StudyHoursPerWeek <= 168),
         AttendanceRate DECIMAL(5,2) NOT NULL CHECK (AttendanceRate >= 0 AND AttendanceRate <= 100),
         GPA DECIMAL(3,2) NOT NULL CHECK (GPA >= 0 AND GPA <= 4.0),
         Major VARCHAR(100) NOT NULL,
         PartTimeJob BOOLEAN NOT NULL,
         ExtraCurricularActivities BOOLEAN NOT NULL
     );

     CREATE INDEX idx_gpa ON Students_Performance(GPA);
     CREATE INDEX idx_attendance ON Students_Performance(AttendanceRate);
     ```
   - Update the database configuration in `app.py` with your MySQL credentials:
     ```python
     db_config = {
         'host': 'localhost',
         'user': 'root',
         'password': 'your_mysql_password',
         'database': 'student_performance'
     }
     ```

4. **Run the Application**:
   Start the Flask server:
   ```bash
   python app.py
   ```
   Access the app at `http://localhost:5000`.

## Usage
- **Home Page (`/`)**: Provides an overview with navigation to manage students or view visualizations.

- **Students Page (`/students`)**:
  - Add new student records using the form.
  - View all student records in a table.
  - **Screenshot**:
    ![Students Page](images/students.png)

- **Visualizations Page (`/visualizations`)**:
  - View GPA Distribution (histogram) and Attendance vs. GPA (scatter plot).
  - **Screenshot** (GPA Distribution shown; scatter plot follows on the same page):
    ![Visualizations Page](images/visualizations.png)

- **API Access (`/api/students`)**:
  - Retrieve all student records in JSON format:
    ```bash
    curl http://localhost:5000/api/students
    ```

## Project Structure
```
student-performance-management/
├── app.py                  # Main Flask application
├── schema.sql              # Database schema
├── clean_csv.py            # Script to validate and clean CSV data
├── templates/
│   ├── index.html          # Home page
│   ├── students.html       # Manage students page
│   └── visualizations.html # Visualizations page
├── static/
│   └── charts.js           # JavaScript for rendering charts
├── images/
│   ├── students.png        # Screenshot of Students page
│   └── visualizations.png  # Screenshot of Visualizations page
└── README.md               # Project documentation
```

## Importing CSV Data
To import student data from a CSV file:
1. Prepare a CSV file with the following columns: `StudentID,Gender,Age,StudyHoursPerWeek,AttendanceRate,GPA,Major,PartTimeJob,ExtraCurricularActivities`.
   Example:
   ```csv
   StudentID,Gender,Age,StudyHoursPerWeek,AttendanceRate,GPA,Major,PartTimeJob,ExtraCurricularActivities
   1,M,18,20,95.5,3.75,Computer Science,1,0
   2,F,19,15,88.0,3.20,Mathematics,0,1
   ```

2. Validate and clean the CSV using the provided script:
   ```bash
   python clean_csv.py
   ```
   This generates `students_cleaned.csv` after validation.

3. Import the cleaned CSV into MySQL:
   - **Using MySQL Command Line**:
     ```sql
     LOAD DATA INFILE '/path/to/students_cleaned.csv'
     INTO TABLE Students_Performance
     FIELDS TERMINATED BY ',' 
     ENCLOSED BY '"' 
     LINES TERMINATED BY '\n'
     IGNORE 1 LINES
     (StudentID, Gender, Age, StudyHoursPerWeek, AttendanceRate, GPA, Major, PartTimeJob, ExtraCurricularActivities);
     ```
   - **Using MySQL Workbench**: Use the "Table Data Import Wizard" to import `students_cleaned.csv`.

4. Verify the import:
   ```sql
   SELECT * FROM Students_Performance LIMIT 5;
   ```

## Visualizations
The `/visualizations` page provides two charts:
- **GPA Distribution**: A histogram showing the distribution of GPAs across students.
- **Attendance vs. GPA**: A scatter plot illustrating the relationship between attendance rate and GPA.

**Note**: Visualizations require data in the `Students_Performance` table. If no data is present, a message will be displayed.

## Contributing
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes and commit:
   ```bash
   git commit -m "Add your feature"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/your-feature-name
   ```
5. Open a Pull Request on GitHub.

Please ensure your code follows PEP 8 style guidelines and includes appropriate documentation.
