import os
import csv
import django
import logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "senior_project_app.settings")
django.setup()

from django.contrib.auth.models import User
from projects.models import Student, Advisor, Project, Skill
from django.contrib.contenttypes.models import ContentType

# Setup logging
logging.basicConfig(
    filename="import_log.txt",
    filemode="w",  # Overwrite each time
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log(message):
    print(message)  # Show on console
    logging.info(message)

# CSV Directory
CSV_DIR = os.path.join(os.path.dirname(__file__), "csv_data")

def import_students():
    """Bulk import students from students.csv"""
    csv_file = os.path.join(CSV_DIR, "students.csv")

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            username = row["username"]
            password = row["password"]
            project_title = row.get("project_title", "").strip()

            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                log(f"✅ Created user: {username}")

            student, student_created = Student.objects.get_or_create(user=user)

            if project_title:
                try:
                    project = Project.objects.get(title=project_title)
                    student.created_project = project
                    student.save()
                    log(f"✅ Linked {username} to project '{project_title}'")
                except Project.DoesNotExist:
                    log(f"⚠️ Warning: Project '{project_title}' not found for student {username}.")

            if student_created:
                log(f"✅ Created Student entry for user: {username}")


def import_advisors():
    """Bulk import advisors from advisors.csv"""
    csv_file = os.path.join(CSV_DIR, "advisors.csv")

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            username = row["username"].strip()
            password = row["password"].strip()

            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                log(f"✅ Created user: {username}")

            advisor, advisor_created = Advisor.objects.get_or_create(user=user)

            if advisor_created:
                log(f"✅ Created Advisor entry for user: {username}")
            else:
                log(f"⚠️ Skipping duplicate advisor entry: {username}")


def import_skills():
    """Bulk import skills from skills.csv"""
    csv_file = os.path.join(CSV_DIR, "skills.csv")

    with open(csv_file, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        existing_skills = set(Skill.objects.values_list("name", flat=True))
        skills_to_create = []

        for row in reader:
            skill_name = row["name"].strip()
            if skill_name and skill_name not in existing_skills:
                skills_to_create.append(Skill(name=skill_name))

        if skills_to_create:
            Skill.objects.bulk_create(skills_to_create)
            log(f"✅ Successfully imported {len(skills_to_create)} new skills")
        else:
            log("⚠️ No new skills to import (all already exist)")


def import_advisor_projects():
    """Bulk import advisor-created projects from advisor_projects.csv"""
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
            skills_required = [s.strip() for s in row["skills_required"].split(",")]

            try:
                advisor = Advisor.objects.get(user__username=advisor_username)
            except Advisor.DoesNotExist:
                log(f"⚠️ Advisor '{advisor_username}' not found. Skipping project '{title}'.")
                continue

            author_type = ContentType.objects.get_for_model(Advisor)

            project, created = Project.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "status": status,
                    "member_limit": member_limit,
                    "advisor": advisor,
                    "author_type": author_type,
                    "author_id": advisor.id
                }
            )

            if created:
                for skill_name in skills_required:
                    skill, _ = Skill.objects.get_or_create(name=skill_name)
                    project.skills_required.add(skill)

                project.update_status()
                projects_created += 1
                log(f"✅ Created project: {title} (Advisor: {advisor_username})")
            else:
                log(f"⚠️ Skipping duplicate project: {title}")

    log(f"🎉 Successfully imported {projects_created} advisor-created projects")


if __name__ == "__main__":
    log("🚀 Starting bulk import...")

    import_students()
    import_advisors()
    import_skills()
    import_advisor_projects()

    log("🎉 Data import complete!")
