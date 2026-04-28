"""Minimal CLI interface for AI Thinking Partner."""

from datetime import datetime

from services.habit_service import (
    create_habit,
    list_habits,
)
from services.entry_service import upsert_entry, add_timer_session
from services.progress_service import get_daily_progress


def print_menu():
    print("\n==== AI Thinking Partner ====")
    print("1. Create Habit")
    print("2. List Habits")
    print("3. Log Entry")
    print("4. Add Timer Session")
    print("5. Show Daily Progress")
    print("6. Exit")


def input_date():
    date = input("Enter date (YYYY-MM-DD) or leave empty for today: ").strip()
    if not date:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    return date


def handle_create_habit():
    name = input("Habit name: ").strip()
    habit_type = input("Habit type: ").strip()

    meta = {}

    if habit_type == "duration":
        meta["unit"] = input("Unit (minutes/hours): ").strip()

    elif habit_type == "scale":
        meta["scale_min"] = int(input("Scale min: "))
        meta["scale_max"] = int(input("Scale max: "))

    elif habit_type == "signed_scale":
        meta["scale_min"] = int(input("Scale min: "))
        meta["scale_max"] = int(input("Scale max: "))

    elif habit_type == "timer":
        meta["minimum_minutes"] = int(input("Minimum minutes: "))

    elif habit_type == "count":
        unit_label = input("Unit label (optional): ").strip()
        if unit_label:
            meta["unit_label"] = unit_label

    habit_id = create_habit(name, habit_type, meta)
    print(f"Habit created with ID: {habit_id}")


def handle_list_habits():
    habits = list_habits()
    if not habits:
        print("No habits found.")
        return

    for h in habits:
        print(f"{h['id']} | {h['name']} | {h['type']} | meta={h['meta']}")


def handle_log_entry():
    habit_id = input("Habit ID: ").strip()
    date = input_date()
    value = input("Value: ").strip()

    # Convert numeric types safely
    if value.isdigit():
        value = int(value)

    upsert_entry(habit_id, date, value)
    print("Entry logged.")


def handle_timer_session():
    habit_id = input("Habit ID (timer type): ").strip()
    date = input_date()
    seconds = int(input("Seconds to add: ").strip())

    add_timer_session(habit_id, date, seconds)
    print("Timer session added.")


def handle_daily_progress():
    date = input_date()
    progress = get_daily_progress(date)

    print("\n--- Daily Progress ---")
    print(f"Date: {progress['date']}")
    print(f"Completed: {progress['completed']} / {progress['total']}")
    print(f"Percentage: {progress['percentage']}%")

    print("\nDetails:")
    for d in progress["details"]:
        status = "✓" if d["complete"] else "✗"
        print(f"{status} {d['name']} ({d['type']}) | value={d['value']}")


def main():
    while True:
        print_menu()
        choice = input("Choose option: ").strip()

        try:
            if choice == "1":
                handle_create_habit()
            elif choice == "2":
                handle_list_habits()
            elif choice == "3":
                handle_log_entry()
            elif choice == "4":
                handle_timer_session()
            elif choice == "5":
                handle_daily_progress()
            elif choice == "6":
                print("Exiting...")
                break
            else:
                print("Invalid choice.")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
