""" Thisis unittest . py file which is testing the functions of the file which 
 have been declaredd"""
import os
import unittest
from typing import Iterator, Tuple, Dict, List
from Student_Repository_Shraddha_Gabani import Repository, Studs, Insts, file_reader,MajorC

class TestRepository(unittest.TestCase):
    """Path setup"""
    def setUp(self):
            self.test_path = "D:\\810"
            self.db_path = 'D:\\810\\hw11.db'
            self.repo = Repository(self.test_path,False,self.db_path)
        
    def test_majors(self):
        """ Testing majors table"""
        result1 = [['SFEN', ['SSW 540', 'SSW 555', 'SSW 810'], ['CS 501', 'CS 546']], ['CS', ['CS 546', 'CS 570'], ['SSW 565', 'SSW 810']]]

        result2 = [majors.ptable_row() for majors in self.repo._majord.values()]
    
        self.assertEqual(result1,result2)

    def test_Student_attributes(self):
        """ Testing student table """
        result1 = {'10103': ['10103', 'Jobs, S', 'SFEN', ['CS 501', 'SSW 810'], ['SSW 540', 'SSW 555'], [], 3.38],
                   '10115': ['10115', 'Bezos, J', 'SFEN', ['SSW 810'], ['SSW 540', 'SSW 555'], ['CS 501', 'CS 546'], 2.0],
                   '10183': ['10183', 'Musk, E', 'SFEN', ['SSW 555', 'SSW 810'], ['SSW 540'], ['CS 501', 'CS 546'], 4.0],
                   '11714': ['11714', 'Gates, B', 'CS', ['CS 546', 'CS 570', 'SSW 810'], [], [], 3.5]}
       
        calculated = {cwid: studs.ptable_row() for cwid, studs in self.repo._studs.items()}
    
        self.assertEqual(result1,calculated)

    def test_Instructor(self):
        """Testcase for instructor"""
        result1 = {('98762', 'Hawking, S', 'CS', 'CS 501', 1),
                   ('98764', 'Cohen, R', 'SFEN', 'CS 546', 1),
                   ('98763', 'Rowland, J', 'SFEN', 'SSW 555', 1),
                   ('98762', 'Hawking, S', 'CS', 'CS 546', 1),
                   ('98762', 'Hawking, S', 'CS', 'CS 570', 1),
                   ('98763', 'Rowland, J', 'SFEN', 'SSW 810', 4)}
        calculated = {tuple(detail) for insts in self.repo._insts.values() for detail in insts.ptable_row()}
        self.assertEqual(result1, calculated)

    def test_student_grade(self):
        """Testcase for instructor"""
        result1 = [('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                    ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                    ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                    ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                    ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                    ('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                    ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                    ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                    ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J')]
        calculated = [studs for studs in self.repo._student_summaty_grade(self.db_path)]
        self.assertEqual(result1, calculated)

#execution starts from here
if __name__ == "__main__":
    unittest.main(exit=False, verbosity=2)
