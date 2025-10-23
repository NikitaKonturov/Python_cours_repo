from parser import parse_input
from checker import check_feasibility
from scheduler import schedule_one_day


def main():
    subjects, teachers, groups, classrooms, slots = parse_input("input.json")
    errors = check_feasibility(groups, teachers, classrooms, slots, subjects)
    if errors:
        print("Невозможно составить расписание:")
        for e in errors:
            print(" -", e)
        return

    schedule = schedule_one_day(subjects, teachers, groups, classrooms, slots)
    if schedule is None:
        print("Расписание не найдено: конфликт ресурсов при раскладке.")
    else:
        schedule.to_colored_console()


if __name__ == "__main__":
    main()
