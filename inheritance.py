class Student:
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.marks = []

    def average(self):
        return sum(self.marks)/len(self.marks)

    @classmethod
    def friend(cls, origin, friend_name, **kwargs):
        return cls(friend_name, origin.school, **kwargs)


class WorkingStudent(Student):
    def __init__(self, name, school, salary, job_title):
        super().__init__(name, school)
        self.salary = salary
        self.job_title = job_title

#avant *args 
#anna = Student("Anna","Oxford")

# En utilisant *args
# anna = WorkingStudent("Anna","Oxford",20.00,"developer software")

# en utilisant *kwargs
anna = WorkingStudent("Anna","Oxford",salary = 20.00,job_title = "developer software")
print(anna.salary)

#en utilisant *args
#friend = WorkingStudent.friend(anna,"Greg",17.5,"developer software")

# en utilisant *kwargs
friend = WorkingStudent.friend(anna,"Greg",salary = 17.5, job_title = "developer software")
print(friend.name)
print(friend.school)
print(friend.salary)