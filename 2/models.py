from dataclasses import dataclass
from typing import Optional, Set, List, Dict

# ANSI escape-коды для цветного вывода
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
RESET = "\033[0m"


@dataclass
class Subject:
    id: int
    name: Optional[str] = None


@dataclass
class Teacher:
    id: int
    subjects: Set[int]


@dataclass
class Group:
    id: int
    required_subjects: List[int]


@dataclass
class Classroom:
    id: int


@dataclass(frozen=True)
class ClassSlot:
    index: int


@dataclass
class Lesson:
    teacher_id: int
    group_id: int
    subject_id: int
    classroom_id: int
    slot_index: int


class Schedule:
    def __init__(self, classrooms: List[Classroom], slots: List[ClassSlot]):
        self.classrooms = classrooms
        self.slots = slots
        self.grid: Dict[int, Dict[int, Optional[Lesson]]] = {
            slot.index: {room.id: None for room in classrooms} for slot in slots
        }
        self.teacher_busy: Dict[int, Set[int]] = {}
        self.group_busy: Dict[int, Set[int]] = {}

    def can_place(self, teacher_id: int, group_id: int, classroom_id: int, slot_index: int) -> bool:
        if self.grid[slot_index][classroom_id] is not None:
            return False
        if slot_index in self.teacher_busy.get(teacher_id, set()):
            return False
        if slot_index in self.group_busy.get(group_id, set()):
            return False
        return True

    def place(self, lesson: Lesson):
        self.grid[lesson.slot_index][lesson.classroom_id] = lesson
        self.teacher_busy.setdefault(lesson.teacher_id, set()).add(lesson.slot_index)
        self.group_busy.setdefault(lesson.group_id, set()).add(lesson.slot_index)

    def remove(self, lesson: Lesson):
        self.grid[lesson.slot_index][lesson.classroom_id] = None
        self.teacher_busy[lesson.teacher_id].remove(lesson.slot_index)
        self.group_busy[lesson.group_id].remove(lesson.slot_index)

    # === Цветной вывод ===
    def to_colored_console(self):
        for slot in self.slots:
            print(CYAN + f"\n=== Пара {slot.index} ===" + RESET)
            for room in self.classrooms:
                lesson = self.grid[slot.index][room.id]
                if lesson:
                    print(f"Ауд. {room.id}: "
                          f"{GREEN}Преп. {lesson.teacher_id}{RESET}, "
                          f"{YELLOW}Гр. {lesson.group_id}{RESET}, "
                          f"{MAGENTA}Предм. {lesson.subject_id}{RESET}")
                else:
                    print(f"Ауд. {room.id}: —")
