class Student:
  def __init__(self, name, school):
    self.name = name
    self.school = school
    self.marks = []

  def average(self):
    return sum(self.marks) / len(self.marks)

  def go_to_school(self):
    print("I'm going to {}.".format(self.school))

  @classmethod  
  def to_be_student(cls):
    print("I'm a {}".format(cls))  

  @staticmethod 
  def go_to_classroom():
    print("I'm going to classroom.")

anna = Student("anna",'MIT')  
anna.marks.append(56)
anna.marks.append(71)

anna.go_to_school()
anna.to_be_student()
Student.go_to_classroom()