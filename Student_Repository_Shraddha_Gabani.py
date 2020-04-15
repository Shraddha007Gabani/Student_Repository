"""program is about hired by Stevens Institute of Technology to create a data repository of courses, students, and instructors. """

import os
import sqlite3
from prettytable import PrettyTable
from collections import defaultdict
from typing import Dict,Set,List,Iterator,Tuple,DefaultDict
from HW08_Shraddha_Gabani import file_reader

class Repository:
    
    """ Repository to store information of students and instructors """

    def __init__(self, dire : str, p : bool,db_path : str)->None:
        """ Initialize directory and dictionary """
        s1 : str='students11.txt'
        i1 : str='instructors11.txt'
        g1 : str='grades11.txt'
        m1 : str='majors11.txt'
        self._dire :str = dire
        self.db_path : str = db_path
        self._studs :Dict[str , List[str, Studs]]= dict()
        self._insts :Dict[str ,List[str, Insts]]= dict()
        self._majord :Dict[str ,List[str, MajorC]]= dict()
        

        try:
            self._student_summaty_grade(os.path.join(dire, self.db_path))
            self._get_major(os.path.join(dire, m1))
            self._get_studs(os.path.join(dire, s1))
            self._get_insts(os.path.join(dire, i1))
            self._get_grades(os.path.join(dire, g1))
            
            
        except FileNotFoundError as f:
            raise FileNotFoundError(f)
        else:
            if p:
                self.studs_table()
                self.insts_table()
                self.major_table()
                self.student_grade_table()

    def _get_studs(self, path : str):
        """ Student detail are read using file reading gen and added to dictionary """
        try:
            for cwid, name, major in file_reader(path, 3, sep='\t', header=True):
                if major not in self._majord:
                    print(f"Student {cwid} '{name}' has unknown major '{major}'")
                else:
                    self._studs[cwid] = Studs(cwid, name, self._majord[major])
        except ValueError as v:
            print(f"cant find any the details")
        except FileNotFoundError as f:
            raise FileNotFoundError(f)


    def _get_insts(self, path : str)->None:
        """ take instructor details from the path and add to it """
        try:
            for cwid, name, dept in file_reader(path, 3, sep='\t', header=True):
                self._insts[cwid] = Insts(cwid, name, dept)
        except ValueError:
            print(f"cant find any the details")
        except FileNotFoundError as f:
            raise FileNotFoundError(f)

    def _get_grades(self, path : str)->None:
        """ Read from grade file and assign the values to appropriate student and instructor """
        try:
            for std_cwid, course, grade, ins_cwid in file_reader(path, 4, sep='\t', header=True):
                if std_cwid in self._studs:
                    self._studs[std_cwid].add_course(course, grade)
                else:
                    print(f'Grade for unknown student {std_cwid}')

                if ins_cwid in self._insts:
                    self._insts[ins_cwid].add_studs(course)
                else:
                    print(f'Grade for unknown instructor {ins_cwid}')
        except ValueError:
            print(f"cant find any the details")
        except FileNotFoundError as f:
            raise FileNotFoundError(f)

    def _get_major(self, path : str):
        """Major details are read using file reading gen and added to dictionary"""
        try:
            for major, flag, course in file_reader(path, 3, sep='\t', header=True):
                if major not in self._majord:
                    self._majord[major] = MajorC(major)
                self._majord[major].add_course(course, flag)
        except ValueError:
            print(f"cant find any the details")
        except FileNotFoundError as f:
            raise FileNotFoundError(f)

    def _student_summaty_grade(self,db_path):
        db :sqlite3.Connection = sqlite3.connect(self.db_path)
        queries = """SELECT S.Name,S.CWID,G.Course,G.Grade,I.Name
                    FROM students11 AS S JOIN grades11 AS G ON S.CWID = G.StudentCWID
                    JOIN instructors11 AS I ON G.InstructorCWID=I.CWID
                    order by s.Name"""
        for Name,CWID,Course,Grade,IName in db.execute(queries):
            yield Name,CWID,Course,Grade,IName
        


    def studs_table(self)->PrettyTable:
        """ Summary of student table """
        pt : PrettyTable= PrettyTable(field_names=Studs.ptable_header)
        for studs in self._studs.values():
            pt.add_row(studs.ptable_row())
        return pt

    def insts_table(self)->PrettyTable:
        """ Summary of instructor table """
        pt :PrettyTable= PrettyTable(field_names=Insts.ptable_header)
        for insts in self._insts.values():
            for row in insts.ptable_row():
                pt.add_row(row)

        return pt
    def major_table(self)->PrettyTable:
        """ Summary of major table """
        pt : PrettyTable= PrettyTable(field_names=MajorC.ptable_header)
        for major in self._majord.values():
            pt.add_row(major.ptable_row())
        return pt

    def student_grade_table(self)->PrettyTable:
        """ Summary of student_grade table """
        pt : PrettyTable= PrettyTable(field_names=['NAME','CWID','COURSE','GRADE','Instructor'])
        for studs in self._student_summaty_grade(self.db_path):
            pt.add_row(studs)
        return pt


class Studs:
    """ Student class """
    ptable_header :list= ['CWID', 'Name','major', 'Completed Courses','rem_required', 'rem_electives','gpa']

    def __init__(self, cwid :str, name : str, major :str)->None:
        """ Initialize student details """
        self._cwid : str= cwid
        self._name : str= name
        self._major : str= major
        self._courses : Dict[str,str]= defaultdict()

    def add_course(self, course :str, grade :str)->None:
        """ Add course with grade """
        self._courses[course] = grade

    def gpa(self):
        """calculate the GPA using dictionary"""
        points: Dict[str, float] = {"A": 4.00, "A-": 3.75, "B+": 3.25, "B": 3.00,"B-": 2.75, "C+": 2.25, "C": 2.00, "C-": 0.00,
        "D+": 0.00, "D": 0.00, "D-": 0.00, "F": 0.00}
        try:
            div : int=len(self._courses.values())
            return round((sum([points[grade] for grade in self._courses.values()]) / div),2)
        except ZeroDivisionError as z:
            print(z)

    def ptable_row(self)->None:
        """ Return a row for student's prettytable """
        major, passed, rem_required, rem_electives = self._major.remaining(self._courses)
        return [self._cwid, self._name, major, sorted(passed), sorted(rem_required), sorted(rem_electives),self.gpa()]


class Insts:
    """ Instructor class """
    ptable_header = ['CWID', 'Name', 'Dept', 'Course', 'Students']

    def __init__(self, cwid :int, name : str, dept : str)->None:
        """ Initialize instructor details """
        self._cwid:int = cwid
        self._name :str= name
        self._dept :str = dept
        self._cour :Dict[str] = defaultdict(int)

    def add_studs(self, course :str)->None:
        """ Count the number of students took the course with this instructor """
        self._cour[course] =self._cour[course]+1

    def ptable_row(self)->None:
        """ Yield the rows for instructor prettytable """
        for course, count in self._cour.items():
            yield [self._cwid, self._name, self._dept, course, count]

class MajorC:
    """ Student class """
    ptable_header :list= ['Major', 'Require Cources', 'Elective']
    min_grades = {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}

    def __init__(self, major :str)->None:
        """ Initialize student details """
        self._major : str= major
        self._Requirecourses :Set = set()
        self._Electivecourses : Set= set()

    def add_course(self, course :str ,req :str)->None:
        """ Add course with grade """
        if req== 'R':
            self._Requirecourses.add(course)
        elif req == "E":
            self._Electivecourses.add(course)
        else:
            print(f'Grade for unknolwn instructor')

    def remaining(self, completed : defaultdict())->None:
        """Adding remaining courses as well as electives"""
        passed = {course for course, grade in completed.items() if grade in MajorC.min_grades}
        rem_required = self._Requirecourses - passed
        rem_electives = self._Electivecourses

        if self._Electivecourses.intersection(passed):
            rem_electives = set()

        return self._major, passed, rem_required, rem_electives


    def ptable_row(self)->None:
        """ Return a row for student's prettytable """
        return [self._major, sorted(self._Requirecourses),sorted(self._Electivecourses)]




def main()->None:
    """ Pass the directory to Repository class """
    dire = 'D:\\810\\HW11'
    db_path :str = 'D:\\810\\HW11\\hw11.db'
    o1:Repository=Repository(dire,True,db_path)
    print("student summary")
    print(o1.studs_table())
    print("Instructor summary")
    print(o1.insts_table())
    print("major summary")
    print(o1.major_table())
    print("major summary")
    print(o1.student_grade_table())
    

if __name__ == '__main__':
    """ Run main function on start """
    main()
