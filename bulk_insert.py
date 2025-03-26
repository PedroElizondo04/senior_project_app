import os
import csv
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senior_project_app.settings")
django.setup()

from django.contrib.auth.models import User
from projects.models import Student, Advisor, Project, Skill
from django.contrib.contenttypes.models import ContentType

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

            user, created = User.objects.get_or_create(username=username, defaults={"password": password})

            # Ensure a Student instance is created
            student, student_created = Student.objects.get_or_create(user=user)

            if created:
                print(f"✅ Created user: {username}")
            else:
                print(f"⚠️ Skipping duplicate user: {username}")

            if student_created:
                print(f"✅ Created Student entry for user: {username}")


def import_advisors():
    """Bulk import advisors from advisors.csv"""
    csv_file = os.path.join(CSV_DIR, "advisors.csv")

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            username = row["username"].strip()
            password = row["password"].strip()  # Ensure passwords are hashed

            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)  # Hash the password
                user.save()
                print(f"✅ Created user: {username}")

            # Ensure an Advisor instance is created
            advisor, advisor_created = Advisor.objects.get_or_create(user=user)

            if advisor_created:
                print(f"✅ Created Advisor entry for user: {username}")
            else:
                print(f"⚠️ Skipping duplicate advisor entry: {username}")


def import_skills():
    """Bulk import skills from skills.csv"""
    csv_file = os.path.join(CSV_DIR, "skills.csv")

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        existing_skills = set(Skill.objects.values_list("name", flat=True))  # Get existing skill names
        skills_to_create = []

        for row in reader:
            skill_name = row["name"].strip()
            if skill_name and skill_name not in existing_skills:  # Avoid duplicates
                skills_to_create.append(Skill(name=skill_name))

        if skills_to_create:
            Skill.objects.bulk_create(skills_to_create)
            print(f"✅ Successfully imported {len(skills_to_create)} new skills")
        else:
            print("⚠️ No new skills to import (all already exist)")


def import_advisor_projects():
    """Bulk import advisor-created projects"""
    csv_file = os.path.join(CSV_DIR, "advisor_projects.csv")

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        projects_created = 0

        for row in reader:
            title = row["title"].strip()
            description = row["description"].strip()
            status = row["status"].strip()
            member_limit = int(row["member_limit"])
            advisor_username = row["advisor_username"].strip()
            skills_required = [s.strip() for s in row["skills_required"].split(",")]  # List of skills

            # Get the advisor object (if exists)
            try:
                advisor = Advisor.objects.get(user__username=advisor_username)
            except Advisor.DoesNotExist:
                print(f"⚠️ Warning: Advisor '{advisor_username}' not found. Skipping project '{title}'.")
                continue

            # Get Advisor ContentType
            advisor_content_type = ContentType.objects.get_for_model(Advisor)

            # Create project with author fields
            project, created = Project.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "status": status,
                    "member_limit": member_limit,
                    "advisor": advisor,
                    "author_type": advisor_content_type,  # Set author type to Advisor
                    "author_id": advisor.id,  # Set author ID to Advisor's ID
                }
            )

            if created:
                # Link required skills
                for skill_name in skills_required:
                    skill, _ = Skill.objects.get_or_create(name=skill_name)
                    project.skills_required.add(skill)

                projects_created += 1
                print(f"✅ Created project: {title} (Author: {advisor_username})")
            else:
                print(f"⚠️ Skipping duplicate project: {title}")

    print(f"🎉 Successfully imported {projects_created} advisor-created projects")

if __name__ == "__main__":
    print("🚀 Starting bulk import...")

    import_students()
    import_advisors()
    import_skills()
    import_advisor_projects()  # Inserts advisor-created projects

    print("🎉 Data import complete!")
