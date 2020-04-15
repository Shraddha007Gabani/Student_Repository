"""implement the datetime and time moduleapartfrom ot read the file and also analyze the file by using prettytable"""
from datetime import datetime, timedelta
from typing import Iterator, Tuple, Dict, List
import os
from prettytable import PrettyTable


def date_arithmetic()->tuple:
    """ return the date according to format and days by usinf imbuilt module """
    d1 : datetime = datetime(2020, 2, 27)
    d2 :datetime = datetime(2019, 2, 27)
    d3 :datetime = datetime(2019, 9, 30)
    d4 :datetime = datetime(2019, 2, 1)
    

    three_days_after_02272000: datetime = d1 + timedelta(days=3)
    three_days_after_02272017: datetime = d2 + timedelta(days=3)
    days_passed_01012017_10312017: int = (d3 - d4).days

    return three_days_after_02272000, three_days_after_02272017, days_passed_01012017_10312017


def file_reader(path: str, fields: int, sep: str = ",", header: bool = False)-> Iterator[Tuple[str]]:
    """ generator function file_reader() to read field-separated text files and yield a tuple
        with all of the values from a single line in the file on each call to next(). """
    
    
    try:
        fopen= open(path, "r")
        if not (file := fopen):
            raise FileNotFoundError

        with file:  # close file after opening
            for l_num, line in enumerate(file, 1):
                row_line: List[str] = line.rstrip("\n").split(sep)
                row_line_count: int = len(row_line)
                if row_line_count != fields:
                    raise ValueError(f"{path} has {row_line_count} fields on line {l_num} but expected {fields}")

                if not header or l_num != 1:
                    yield tuple(row_line)
    except FileNotFoundError:
        print(f"File {path} is not found")


class FileAnalyzer:
    """ analyze all the file of directory """
    def __init__(self, directory: str):
        """ store the directory and files summary """
        if not os.path.exists(directory):
            raise FileNotFoundError(f"The specified directory ‘{directory}’ is not found")

        self.directory: str = directory # NOT mandatory!
        self.files_summary: Dict[str, Dict[str, int]] = dict()

        self.analyze_files() # summarize the python files data

    def analyze_files(self):
        """ analyze the file of perticular directory """
        for file in os.listdir(self.directory):
            if file[-3:]==(".py"):
                fopen = open(os.path.join(self.directory, file), "r")
                try:
                    if not (py_file := fopen):
                        raise FileNotFoundError

                    with py_file:  # close file after opening
                        class_count:int=0
                        fun_count:int = 0
                        l_count:int = 0
                        ch_count: int= 0
                        for line in py_file:  # calculate values for the file
                            if line.strip().startswith("class "):
                                class_count =class_count+1
                            elif line.strip().startswith("def "):
                                fun_count=fun_count+1

                            l_count =l_count+1
                            ch_count =ch_count+len(line)

                        self.files_summary[str(os.path.join(self.directory, file))] = {"class": class_count,"function": fun_count,"line": l_count,
                                                                                       "char": ch_count}
                except FileNotFoundError:
                    print(f"File {py_file} is not found or can not be opened")
                fopen.close()


    def pretty_print(self)->PrettyTable:
        """ prettify the data and return the prettytable """
        table_contain: PrettyTable = PrettyTable()
        table_contain.field_names = ["File Name", "Classes", "Functions", "Lines", "Characters"]
        for key, value in self.files_summary.items():
            table_contain.add_row([key] + list(value.values())) 

        return table_contain
    
def main()-> None:
    "call the all function in main"
    d1 :tuple = date_arithmetic()
    print(f"{d1}")
    path="D://810//student_majors.txt"
    for lines in file_reader(path,1,",",True):
        print(f"{lines}")
    obj : FileAnalyzer =FileAnalyzer("D://810")
    print(f"{obj.pretty_print()}")
    

#excution starts from here
if __name__ == '__main__':        
    main()
