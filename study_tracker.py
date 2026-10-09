import json
import os
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

filename = "Study_Tracker.json"


def load_data():
    if os.path.exists(filename):
        with open(filename, "r") as file:
            return json.load(file)
    return {}


def save_data(data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def add_hours(subject, hours):
    data = load_data()

    today = datetime.today().date().isoformat()

    if today not in data:
        data[today] = {}

    if subject in data[today]:
        data[today][subject] += hours
    else:
        data[today][subject] = hours

    save_data(data)

    print(
        f"Added {hours} hrs to {subject} for {today}."
    )


def view_stats():
    data = load_data()

    if not data:
        print("No study hours logged yet.")
        return

    subject_totals = {}

    for day in data.values():
        for subject, hours in day.items():
            subject_totals[subject] = subject_totals.get(subject, 0) + hours

    total = 0

    print("\nStudy Summary\n")

    for subject, hours in subject_totals.items():
        print(f"{subject}: {hours:.1f} hrs")
        total += hours

    print(f"\nTotal Study Time: {total:.1f} hrs")


def plot_7_days():
    data = load_data()

    today = datetime.today().date()

    last_7_days = [
        (today - timedelta(days=i)).isoformat()
        for i in range(6, -1, -1)
    ]

    daily_totals = []

    for day in last_7_days:
        if day in data:
            daily_totals.append(sum(data[day].values()))
        else:
            daily_totals.append(0)

    avg = sum(daily_totals) / 7
    peak = max(daily_totals)

    plt.figure(figsize=(8, 4))
    plt.bar(last_7_days, daily_totals)

    plt.xticks(rotation=45)
    plt.xlabel("Date")
    plt.ylabel("Hours")
    plt.title(
        f"Study Hours (Last 7 Days)\nAverage: {avg:.2f} hrs | Peak: {peak:.2f} hrs"
    )

    plt.tight_layout()
    plt.show()


def predict():
    data = load_data()

    today = datetime.today().date()

    week = [
        (today - timedelta(days=i)).isoformat()
        for i in range(6, -1, -1)
    ]

    total = 0

    for day in week:
        if day in data:
            total += sum(data[day].values())

    avg = total / 7

    projected = avg * 7

    print(f"\nAverage per day: {avg:.2f} hrs")
    print(f"Projected weekly study time: {projected:.2f} hrs")


def main():

    while True:

        print("\n1. Add Study Hours")
        print("2. View Statistics")
        print("3. Show Last 7 Days Graph")
        print("4. Weekly Prediction")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            subject = input("Subject: ").strip()

            try:
                hours = float(input("Hours: "))
                add_hours(subject, hours)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "2":
            view_stats()

        elif choice == "3":
            plot_7_days()

        elif choice == "4":
            predict()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()