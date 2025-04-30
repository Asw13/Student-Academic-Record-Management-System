from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'watambe13aw',
    'database': 'student_performance'
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Students route for data entry and viewing
@app.route('/students', methods=['GET', 'POST'])
def students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch students
    cursor.execute("SELECT * FROM Students_Performance")
    students = cursor.fetchall()
    
    if request.method == 'POST':
        student_id = request.form['StudentID']
        gender = request.form['Gender']
        age = request.form['Age']
        study_hours = request.form['StudyHoursPerWeek']
        attendance_rate = request.form['AttendanceRate']
        gpa = request.form['GPA']
        major = request.form['Major']
        part_time_job = 1 if request.form.get('PartTimeJob') == 'on' else 0
        extra_activities = 1 if request.form.get('ExtraCurricularActivities') == 'on' else 0
        
        try:
            cursor.execute(
                """
                INSERT INTO Students_Performance 
                (StudentID, Gender, Age, StudyHoursPerWeek, AttendanceRate, GPA, Major, PartTimeJob, ExtraCurricularActivities)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (student_id, gender, age, study_hours, attendance_rate, gpa, major, part_time_job, extra_activities)
            )
            conn.commit()
        except Error as e:
            print(f"Error inserting student: {e}")
        
        return redirect(url_for('students'))
    
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)

# Visualizations route
@app.route('/visualizations')
def visualizations():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Fetch data for visualizations
    cursor.execute("SELECT GPA FROM Students_Performance")
    gpa_data = [row['GPA'] for row in cursor.fetchall()]
    
    cursor.execute("SELECT AttendanceRate, GPA FROM Students_Performance")
    attendance_gpa = [{'x': row['AttendanceRate'], 'y': row['GPA']} for row in cursor.fetchall()]
    
    cursor.close()
    conn.close()
    
    return render_template('visualizations.html', gpa_data=gpa_data, attendance_gpa=attendance_gpa)

# API endpoint for data
@app.route('/api/students')
def api_students():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Students_Performance")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(students)

if __name__ == '__main__':
    app.run(debug=True)