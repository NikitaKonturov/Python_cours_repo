from typing import List, Optional, Tuple, Dict
from models import Subject, Teacher, Group, Classroom, ClassSlot, Lesson, Schedule


def build_requirements(groups: List[Group]) -> List[Tuple[int, int]]:
    return [(g.id, s) for g in groups for s in g.required_subjects]


def teacher_candidates(teachers: List[Teacher], subject_id: int) -> List[int]:
    return [t.id for t in teachers if subject_id in t.subjects]


def schedule_one_day(subjects, teachers, groups, classrooms, slots) -> Optional[Schedule]:
    reqs = build_requirements(groups)
    teacher_by_subject: Dict[int, List[int]] = {
        s.id: teacher_candidates(teachers, s.id) for s in subjects
    }
    reqs.sort(key=lambda rs: len(teacher_by_subject[rs[1]]))
    schedule = Schedule(classrooms, slots)

    def backtrack(idx: int) -> bool:
        if idx == len(reqs):
            return True
        group_id, subj_id = reqs[idx]
        for teacher_id in teacher_by_subject[subj_id]:
            for slot in slots:
                for room in classrooms:
                    if schedule.can_place(teacher_id, group_id, room.id, slot.index):
                        lesson = Lesson(teacher_id, group_id, subj_id, room.id, slot.index)
                        schedule.place(lesson)
                        if backtrack(idx + 1):
                            return True
                        schedule.remove(lesson)
        return False

    return schedule if backtrack(0) else None
