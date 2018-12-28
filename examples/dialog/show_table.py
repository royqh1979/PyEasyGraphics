from easygraphics.dialog import *


class Person:
    def __init__(self, name, age, sex):
        self.name = name
        self.age = age
        self.sex = sex


objs = [Person("Jack", 22, "M"), Person("Micheal", 40, "F"), Person("David", 24, "M")]
show_table(title="peoples", datas=objs, fields=["name", "age", "sex"], field_names=["NAME", "AGE", "SEX"])
