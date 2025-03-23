import os
import csv
import django
from django.contrib.auth.models import User
from your_app.models import Student, Advisor, Project, Skill

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senior_project_app.settings")
django.setup()

# Directory where CSV files are stored
CSV_DIR = os.path.join(os.path.dirname(__file__), "csv_data")


def import_students():
    """Bulk import students from students.csv"""
    csv_file = os.path.join(CSV_DIR, "students.csv")
    students = []

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row["username"]
            password = row["password"]

            # Create a new user and hash the password
            user = User.objects.create_user(username=username, password=password)

            # Create a student linked to the user
            students.append(Student(user=user))

    Student.objects.bulk_create(students)
    print(f"✅ Successfully imported {len(students)} students")


def import_advisors():
    """Bulk import advisors from advisors.csv"""
    csv_file = os.path.join(CSV_DIR, "advisors.csv")
    advisors = []

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row["username"]
            password = row["password"]
            bio = row["bio"]

            # Create a new user and hash the password
            user = User.objects.create_user(username=username, password=password)

            # Create an advisor linked to the user
            advisors.append(Advisor(user=user, bio=bio))

    Advisor.objects.bulk_create(advisors)
    print(f"✅ Successfully imported {len(advisors)} advisors")


def import_projects():
    """Bulk import projects from projects.csv"""
    csv_file = os.path.join(CSV_DIR, "projects.csv")
    projects = []

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["title"]
            description = row["description"]
            status = row["status"]
            member_limit = int(row["member_limit"])
            advisor_username = row["advisor_username"]

            # Get the advisor object (if exists)
            advisor = None
            if advisor_username:
                try:
                    advisor = Advisor.objects.get(user__username=advisor_username)
                except Advisor.DoesNotExist:
                    print(f"⚠️ Warning: Advisor '{advisor_username}' not found. Skipping advisor assignment.")

            projects.append(Project(title=title, description=description, status=status, member_limit=member_limit, advisor=advisor))

    Project.objects.bulk_create(projects)
    print(f"✅ Successfully imported {len(projects)} projects")


def import_skills():
    """Bulk import skills from skills.csv"""
    csv_file = os.path.join(CSV_DIR, "skills.csv")
    skills = []

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            skills.append(Skill(name=row["name"]))

    Skill.objects.bulk_create(skills)
    print(f"✅ Successfully imported {len(skills)} skills")


if __name__ == "__main__":
    print("🚀 Starting bulk import...")

    import_students()
    import_advisors()
    import_projects()
    import_skills()

    print("🎉 Data import complete!")