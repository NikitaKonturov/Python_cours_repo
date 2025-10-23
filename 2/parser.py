import json
from models import Subject, Teacher, Group, Classroom, ClassSlot


def parse_input(path: str):
    with open(path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    subjects = [Subject(id=i) for i in range(1, raw["Subjects"] + 1)]
    teachers = [Teacher(id=int(t), subjects=set(raw["Teachers"][t])) for t in raw["Teachers"]]
    groups = [Group(id=int(g), required_subjects=list(raw["Groups"][g])) for g in raw["Groups"]]
    classrooms = [Classroom(id=i) for i in range(1, raw["Classrooms"] + 1)]
    slots = [ClassSlot(index=i) for i in range(1, raw["Classes"] + 1)]
    return subjects, teachers, groups, classrooms, slots
