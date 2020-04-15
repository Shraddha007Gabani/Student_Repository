"""program is about hired by Stevens Institute of Technology to create a data repository of courses, students, and instructors. """

import os
from prettytable import PrettyTable
from collections import defaultdict
from HW08_Shraddha_Gabani import file_reader


class Repository:
    
    """ Repository to store information of students and instructors """

    def __init__(self, dire : str, p : bool)->None:
        """ Initialize directory and dictionary """
        s1 : str='students.txt'
        i1 : str='instructors.txt'
        g1 : str='grades.txt'
        self._dire :str = dire
        self._studs :Dict[str , List[str, int]]= dict()
        self._insts :Dict[str ,List[str, int]]= dict()

        try:
            self._get_studs(os.path.join(dire, s1))
            self._get_insts(os.path.join(dire, i1))
            self._get_grades(os.path.join(dire, g1))
        except FileNotFoundError as f:
            raise FileNotFoundError(f)
        else:
            if p:
                self.studs_table()
                self.insts_table()

    def _get_studs(self, path : str)->None:
        """ take student details from the path and add to it"""
        try:
            for cwid, name, major in file_reader(path, 3, sep='\t', header=False):
                self._studs[cwid] = Studs(cwid, name, major)
        except ValueError:
            print(f"cant find any the details ")
        except FileNotFoundError as f:
            raise FileNotFoundError(f)

    def _get_insts(self, path : str)->None:
        """ take instructor details from the path and add to it """
        try:
            for cwid, name, dept in file_reader(path, 3, sep='\t', header=False):
                self._insts[cwid] = Insts(cwid, name, dept)
        except ValueError:
            print(f"cant find any the details")
        except FileNotFoundError as f:
            raise FileNotFoundError(f)

    def _get_grades(self, path : str)->None:
        """ Read from grade file and assign the values to appropriate student and instructor """
        try:
            for std_cwid, course, grade, ins_cwid in file_reader(path, 4, sep='\t', header=False):
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


class Studs:
    """ Student class """
    ptable_header :list= ['CWID', 'Name', 'Completed Courses']

    def __init__(self, cwid :str, name : str, major :str)->None:
        """ Initialize student details """
        self._cwid : str= cwid
        self._name : str= name
        self._major : str= major
        self._courses : Dict[str]= dict()

    def add_course(self, course :str, grade :str)->None:
        """ Add course with grade """
        self._courses[course] = grade

    def ptable_row(self)->None:
        """ Return a row for student's prettytable """
        return [self._cwid, self._name, sorted(self._courses.keys())]


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


def main()->None:
    """ Pass the directory to Repository class """
    dire = 'D:\\810\\HW09'
    o1:Repository=Repository(dire,True)
    print("student summary")
    print(o1.studs_table())
    print("Instructor summary")
    print(o1.insts_table())

if __name__ == '__main__':
    """ Run main function on start """
    main()
