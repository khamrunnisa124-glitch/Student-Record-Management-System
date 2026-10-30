import json
import csv
from pathlib import Path

DATA_FILE = Path("students.json")
CSV_FILE = Path("students_export.csv")


def load_students():
    """Load student records from JSON file."""
    try:
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)
                return data if isinstance(data, list) else []
        return []
    except (json.JSONDecodeError, OSError) as error:
        print("Could not load student data:", error)
        return []


def save_students(students):
    """Save student records to JSON file."""
    try:
        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(students, file, indent=4)
        return True
    except OSError as error:
        print("Could not save student data:", error)
        return False


def add_student(students):
    try:
        student_id = input("Enter student ID: ").strip()
        if not student_id:
            print("Student ID cannot be empty.")
            return
        if any(s["id"] == student_id for s in students):
            print("That student ID already exists.")
            return

        name = input("Enter student name: ").strip()
        course = input("Enter course: ").strip()
        marks = float(input("Enter marks (0-100): "))

        if not name or not course:
            print("Name and course cannot be empty.")
            return
        if not 0 <= marks <= 100:
            print("Marks must be between 0 and 100.")
            return

        students.append({
            "id": student_id,
            "name": name,
            "course": course,
            "marks": marks
        })
        if save_students(students):
            print("Student added successfully.")
    except ValueError:
        print("Invalid marks. Please enter a number.")
    finally:
        print("Add operation finished.")


def view_students(students):
    if not students:
        print("No student records found.")
        return

    # List comprehension creates a formatted list of student records.
    formatted = [
        f'ID: {s["id"]} | Name: {s["name"]} | Course: {s["course"]} | Marks: {s["marks"]}'
        for s in students
    ]
    print("\n--- Student Records ---")
    for record in formatted:
        print(record)


def update_student(students):
    student_id = input("Enter the student ID to update: ").strip()
    student = next((s for s in students if s["id"] == student_id), None)

    if student is None:
        print("Student not found.")
        return

    try:
        new_name = input(f'New name [{student["name"]}]: ').strip()
        new_course = input(f'New course [{student["course"]}]: ').strip()
        new_marks = input(f'New marks [{student["marks"]}]: ').strip()

        if new_name:
            student["name"] = new_name
        if new_course:
            student["course"] = new_course
        if new_marks:
            marks = float(new_marks)
            if not 0 <= marks <= 100:
                print("Marks must be between 0 and 100.")
                return
            student["marks"] = marks

        if save_students(students):
            print("Student updated successfully.")
    except ValueError:
        print("Invalid marks. Please enter a number.")


def delete_student(students):
    student_id = input("Enter the student ID to delete: ").strip()
    student = next((s for s in students if s["id"] == student_id), None)

    if student is None:
        print("Student not found.")
        return

    students.remove(student)
    if save_students(students):
        print("Student deleted successfully.")


def export_to_csv(students):
    if not students:
        print("No records to export.")
        return

    try:
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            fieldnames = ["id", "name", "course", "marks"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)
        print(f"Export successful: {CSV_FILE.resolve()}")
    except OSError as error:
        print("CSV export failed:", error)


def show_topper(students):
    if not students:
        print("No student records found.")
        return
    # Lambda function selects the student with the highest marks.
    topper = max(students, key=lambda s: s["marks"])
    print(f'Topper: {topper["name"]} ({topper["marks"]} marks)')


def main():
    students = load_students()

    while True:
        print("\n===== STUDENT RECORD MANAGEMENT =====")
        print("1. Add student")
        print("2. View students")
        print("3. Update student")
        print("4. Delete student")
        print("5. Export to CSV")
        print("6. Show topper")
        print("7. Exit")

        try:
            choice = input("Choose an option (1-7): ").strip()

            if choice == "1":
                add_student(students)
            elif choice == "2":
                view_students(students)
            elif choice == "3":
                update_student(students)
            elif choice == "4":
                delete_student(students)
            elif choice == "5":
                export_to_csv(students)
            elif choice == "6":
                show_topper(students)
            elif choice == "7":
                print("Thank you for using the system!")
                break
            else:
                print("Please choose a number from 1 to 7.")
        except (KeyboardInterrupt, EOFError):
            print("\nProgram stopped safely.")
            break


if __name__ == "__main__":
    main()
