import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senior_project_app.settings")
django.setup()

from django.contrib.auth.models import User
from projects.models import Student, Advisor, Project, Skill

# Directory where CSV files are stored
CSV_DIR = os.path.join(os.path.dirname(__file__), "csv_data")


def import_students():
    """Bulk import students from students.csv"""
    csv_file = os.path.join(CSV_DIR, "students.csv")

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            username = row["username"]
            password = row["password"]  # Ensure passwords are hashed

            if not User.objects.filter(username=username).exists():  # Avoid duplicate usernames
                User.objects.create_user(username=username, password=password)
                print(f"✅ Created user: {username}")
            else:
                print(f"⚠️ Skipping duplicate user: {username}")


def import_advisors():
    """Bulk import advisors from advisors.csv"""
    csv_file = os.path.join(CSV_DIR, "advisors.csv")

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            username = row["username"].strip()
            password = row["password"].strip()  # Ensure passwords are hashed

            user, created = User.objects.get_or_create(username=username, defaults={"password": password})

            if created:
                print(f"✅ Created advisor: {username}")
            else:
                print(f"⚠️ Skipping duplicate advisor: {username}")


def import_skills():
    """Bulk import skills from skills.csv"""
    csv_file = os.path.join(CSV_DIR, "skills.csv")
    skills = []

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        existing_skills = set(Skill.objects.values_list("name", flat=True))  # Get existing skill names

        for row in reader:
            skill_name = row["name"]
            if skill_name not in existing_skills:  # Avoid duplicates
                skills.append(Skill(name=skill_name))

    if skills:
        Skill.objects.bulk_create(skills)
        print(f"✅ Successfully imported {len(skills)} new skills")
    else:
        print("⚠️ No new skills to import (all already exist)")


def import_advisor_projects():
    """Bulk import advisor-created projects"""
    csv_file = os.path.join(CSV_DIR, "advisor_projects.csv")
    projects = []

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            title = row["title"]
            description = row["description"]
            status = row["status"]
            member_limit = int(row["member_limit"])
            advisor_username = row["advisor_username"]
            skills_required = row["skills_required"].split(", ")  # List of skills

            # Get the advisor object (if exists)
            try:
                advisor = Advisor.objects.get(user__username=advisor_username)
            except Advisor.DoesNotExist:
                print(f"⚠️ Warning: Advisor '{advisor_username}' not found. Skipping.")
                continue

            project = Project(title=title, description=description, status=status, member_limit=member_limit, advisor=advisor)
            project.save()

            # Add required skills
            for skill_name in skills_required:
                skill, _ = Skill.objects.get_or_create(name=skill_name)
                project.skills_required.add(skill)

            projects.append(project)

    print(f"✅ Successfully imported {len(projects)} advisor-created projects")


if __name__ == "__main__":
    print("🚀 Starting bulk import...")

    import_students()
    import_advisors()
    import_skills()
    import_advisor_projects()  # Inserts advisor-created projects

    print("🎉 Data import complete!")
