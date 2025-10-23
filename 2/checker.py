from typing import List
from models import Group, Teacher, Subject, Classroom, ClassSlot


def check_feasibility(groups: List[Group], teachers: List[Teacher],
                      classrooms: List[Classroom], slots: List[ClassSlot],
                      subjects: List[Subject]) -> List[str]:
    errors = []
    total_required = sum(len(g.required_subjects) for g in groups)
    max_capacity = len(classrooms) * len(slots)
    if total_required > max_capacity:
        errors.append(f"Невместимость: требуется {total_required}, доступно {max_capacity}.")

    teacher_by_subject = {s.id: [t.id for t in teachers if s.id in t.subjects] for s in subjects}
    for g in groups:
        for subj in g.required_subjects:
            if not teacher_by_subject.get(subj):
                errors.append(f"Группа {g.id} требует предмет {subj}, но нет преподавателя.")
    return errors
