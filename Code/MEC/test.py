# list1 = [1,2,3,4,5,6]
# list2 = [1,2,3,7,8,9]
# list3 = [i for i in list2 if i not in list1]
# list4 = [i for i in list2 if i in list1]
from dataclasses import dataclass
from typing import Set

# print(list3)
# print(list4)

# @dataclass
# class Student:
#     name: str
#     age: int
#
#     def __hash__(self):
#         return hash(self.name)

# s1 = Student("Darshil Mehta", 21)
# s2 = Student("Harsh Khatana", 23)
# s3 = Student("Ajaat Kaushikeya", 22)
# s4 = Student("Darshil Mehta", 21)
#
# set1: Set[Student] = {s1,s2}
# set2: Set[Student] = {s3,s4}
# set3: Set[Student] = set1 - set2
# set1 = {Student("Darshil Mehta", 21), Student("Harsh Khatana", 23)}
# set2 = {Student("Ajaat Kaushikeya", 22), Student("Darshil Mehta", 21)}

# print(set1-set2)
# print(s1 == s4)
# print(set3)

# @dataclass
# class Test:
#     a: int
#     b: int
#
# test = Test(6,9)
# print(test)
#
# def changeTest(test: Test):
#     test.a -= 6
#     test.b -= 9
#
# changeTest(test) #pass by reference
# print(test)