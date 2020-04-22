from flask import Flask,render_template
import sqlite3
from typing import Dict

DB_file : str = 'D:\\810\\hw12\\hw11.db'

app: Flask = Flask(__name__)

@app.route('/completed')
def completed_courses()-> str:
    query = """SELECT S.Name,S.CWID,G.Course,G.Grade,I.Name
                    FROM students11 AS S JOIN grades11 AS G ON S.CWID = G.StudentCWID
                    JOIN instructors11 AS I ON G.InstructorCWID=I.CWID
                    order by s.Name"""
    db: sqlite3.Connection = sqlite3.connect(DB_file)

    data : Dict[str , str] =[{'name': name, 'cwid' : cwid, 'course':course, 'grade':grade, 'instructor':instructor}\
    for name,cwid,course,grade,instructor in db.execute(query)]
    db.close()

    return render_template('student_summary.html',
                           title='stevens Repository',
                           table_title="student,course,grade,instructor",
                           students=data)
if __name__ == '__main__':
    app.run(debug=True)
