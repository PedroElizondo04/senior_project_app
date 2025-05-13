import pytest
from django.contrib.auth.models import User
from projects.models import Student, Advisor, Project
from projects.services import get_user_role, validate_member_limit, can_student_create_project
from django.contrib.contenttypes.models import ContentType


@pytest.mark.django_db
def test_get_user_role_student():
    user = User.objects.create_user("s1")
    Student.objects.create(user=user)
    assert get_user_role(user) == "STUDENT"

@pytest.mark.django_db
def test_get_user_role_advisor():
    user = User.objects.create_user("a1")
    Advisor.objects.create(user=user)
    assert get_user_role(user) == "ADVISOR"

def test_validate_member_limit_happy():
    assert validate_member_limit(2)
    assert validate_member_limit(4)

def test_validate_member_limit_sad():
    assert not validate_member_limit(1)
    assert not validate_member_limit(5)

@pytest.mark.django_db
def test_can_student_create_project_happy():
    student = Student.objects.create(user=User.objects.create_user("new"))
    assert can_student_create_project(student)

@pytest.mark.django_db
def test_can_student_create_project_sad():
    student = Student.objects.create(user=User.objects.create_user("old"))
    content_type = ContentType.objects.get_for_model(Student)
    project = Project.objects.create(
        title="X",
        description="Y",
        member_limit=2,
        author_type=content_type,
        author_id=student.id
    )
    student.created_project = project
    student.save()

    assert not can_student_create_project(student)

