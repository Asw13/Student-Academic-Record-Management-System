import pandas as pd
import sys

# Load CSV file
input_file = 'student_performance_data.csv'
output_file = 'students_cleaned.csv'

try:
    df = pd.read_csv(input_file)
except FileNotFoundError:
    print(f"Error: {input_file} not found.")
    sys.exit(1)

# Expected columns
expected_columns = [
    'StudentID', 'Gender', 'Age', 'StudyHoursPerWeek', 'AttendanceRate',
    'GPA', 'Major', 'PartTimeJob', 'ExtraCurricularActivities'
]

# Check if columns match
if list(df.columns) != expected_columns:
    print(f"Error: CSV columns do not match expected columns: {expected_columns}")
    sys.exit(1)

# Validation functions
def validate_student_id(student_id):
    if not isinstance(student_id, (int, float)) or student_id != int(student_id):
        return False
    return True

def validate_gender(gender):
    return gender in ['Male', 'Female', 'O']

def validate_age(age):
    return isinstance(age, (int, float)) and 15 <= age <= 25

def validate_study_hours(hours):
    return isinstance(hours, (int, float)) and 0 <= hours <= 168

def validate_attendance_rate(rate):
    return isinstance(rate, (int, float)) and 0 <= rate <= 100

def validate_gpa(gpa):
    return isinstance(gpa, (int, float)) and 0 <= gpa <= 4.0

def validate_major(major):
    return isinstance(major, str) and len(major.strip()) > 0 and len(major) <= 100

def validate_boolean(value):
    if isinstance(value, bool):
        return True
    if isinstance(value, (int, float)):
        return value in [0, 1]
    if isinstance(value, str):
        return value.lower() in ['true', 'false', 'yes', 'no', '1', '0']
    return False

# Clean and validate data
errors = []
cleaned_data = []

for index, row in df.iterrows():
    error = False
    cleaned_row = {}

    # Validate StudentID
    if not validate_student_id(row['StudentID']):
        errors.append(f"Row {index + 2}: Invalid StudentID {row['StudentID']}")
        error = True
    else:
        cleaned_row['StudentID'] = int(row['StudentID'])

    # Validate Gender
    if not validate_gender(row['Gender']):
        errors.append(f"Row {index + 2}: Invalid Gender {row['Gender']}")
        error = True
    else:
        cleaned_row['Gender'] = row['Gender']

    # Validate Age
    if not validate_age(row['Age']):
        errors.append(f"Row {index + 2}: Invalid Age {row['Age']}")
        error = True
    else:
        cleaned_row['Age'] = int(row['Age'])

    # Validate StudyHoursPerWeek
    if not validate_study_hours(row['StudyHoursPerWeek']):
        errors.append(f"Row {index + 2}: Invalid StudyHoursPerWeek {row['StudyHoursPerWeek']}")
        error = True
    else:
        cleaned_row['StudyHoursPerWeek'] = int(row['StudyHoursPerWeek'])

    # Validate AttendanceRate
    if not validate_attendance_rate(row['AttendanceRate']):
        errors.append(f"Row {index + 2}: Invalid AttendanceRate {row['AttendanceRate']}")
        error = True
    else:
        cleaned_row['AttendanceRate'] = round(float(row['AttendanceRate']), 2)

    # Validate GPA
    if not validate_gpa(row['GPA']):
        errors.append(f"Row {index + 2}: Invalid GPA {row['GPA']}")
        error = True
    else:
        cleaned_row['GPA'] = round(float(row['GPA']), 2)

    # Validate Major
    if not validate_major(row['Major']):
        errors.append(f"Row {index + 2}: Invalid Major {row['Major']}")
        error = True
    else:
        cleaned_row['Major'] = row['Major'].strip()

    # Validate PartTimeJob
    if not validate_boolean(row['PartTimeJob']):
        errors.append(f"Row {index + 2}: Invalid PartTimeJob {row['PartTimeJob']}")
        error = True
    else:
        if isinstance(row['PartTimeJob'], bool):
            cleaned_row['PartTimeJob'] = 1 if row['PartTimeJob'] else 0
        elif isinstance(row['PartTimeJob'], (int, float)):
            cleaned_row['PartTimeJob'] = int(row['PartTimeJob'])
        else:
            cleaned_row['PartTimeJob'] = 1 if row['PartTimeJob'].lower() in ['true', 'yes', '1'] else 0

    # Validate ExtraCurricularActivities
    if not validate_boolean(row['ExtraCurricularActivities']):
        errors.append(f"Row {index + 2}: Invalid ExtraCurricularActivities {row['ExtraCurricularActivities']}")
        error = True
    else:
        if isinstance(row['ExtraCurricularActivities'], bool):
            cleaned_row['ExtraCurricularActivities'] = 1 if row['ExtraCurricularActivities'] else 0
        elif isinstance(row['ExtraCurricularActivities'], (int, float)):
            cleaned_row['ExtraCurricularActivities'] = int(row['ExtraCurricularActivities'])
        else:
            cleaned_row['ExtraCurricularActivities'] = 1 if row['ExtraCurricularActivities'].lower() in ['true', 'yes', '1'] else 0

    if not error:
        cleaned_data.append(cleaned_row)

# Check for duplicate StudentIDs
student_ids = [row['StudentID'] for row in cleaned_data]
if len(student_ids) != len(set(student_ids)):
    errors.append("Duplicate StudentIDs found in cleaned data")

# Save cleaned data to CSV
if errors:
    print("Errors found during validation:")
    for error in errors:
        print(error)
    sys.exit(1)
else:
    cleaned_df = pd.DataFrame(cleaned_data)
    cleaned_df.to_csv(output_file, index=False)
    print(f"Cleaned CSV saved to {output_file}")