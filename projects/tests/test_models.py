import pytest
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from projects.models import Project, Student, Advisor, ProjectApplication
from django.contrib.contenttypes.models import ContentType


@pytest.mark.django_db
def test_project_update_status_happy():
    advisor_user = User.objects.create_user("advisor", password="pass")
    advisor = Advisor.objects.create(user=advisor_user)

    content_type = ContentType.objects.get_for_model(Advisor)
    project = Project.objects.create(
        title="AI",
        description="test",
        member_limit=2,
        advisor=advisor,
        author_type=content_type,
        author_id=advisor.id,
    )

    s1 = Student.objects.create(user=User.objects.create_user("s1"))
    s2 = Student.objects.create(user=User.objects.create_user("s2"))
    project.students.set([s1, s2])
    project.update_status()

    assert project.status == "active"


@pytest.mark.django_db
def test_project_update_status_sad_missing_students_or_advisor():
    advisor_user = User.objects.create_user("a1")
    advisor = Advisor.objects.create(user=advisor_user)
    content_type = ContentType.objects.get_for_model(Advisor)

    project = Project.objects.create(
        title="ML",
        description="test",
        member_limit=2,
        author_type=content_type,
        author_id=advisor.id
    )

    project.update_status()
    assert project.status == "in_process"


@pytest.mark.django_db
def test_student_accept_application_happy():
    student_user = User.objects.create_user("stu")
    student = Student.objects.create(user=student_user)

    content_type = ContentType.objects.get_for_model(Student)
    project = Project.objects.create(
        title="Test",
        description="desc",
        member_limit=2,
        author_type=content_type,
        author_id=student.id
    )

    app = ProjectApplication.objects.create(student=student, project=project, application_text="Hi")
    student.accept_application(app)
    app.refresh_from_db()

    assert app.status == "accepted"
    assert student.created_project == project


@pytest.mark.django_db
def test_student_accept_application_sad_redundant_accept():
    student = Student.objects.create(user=User.objects.create_user("stu2"))
    content_type = ContentType.objects.get_for_model(Student)

    p1 = Project.objects.create(
        title="P1", description="x", member_limit=2,
        author_type=content_type,
        author_id=student.id
    )
    p2 = Project.objects.create(
        title="P2", description="x", member_limit=2,
        author_type=content_type,
        author_id=student.id
    )

    a1 = ProjectApplication.objects.create(student=student, project=p1, application_text="A")
    a2 = ProjectApplication.objects.create(student=student, project=p2, application_text="B")

    # Accept the first application through model logic
    student.accept_application(a1)

    a1.refresh_from_db()
    a2.refresh_from_db()

    assert a1.status == "accepted"
    assert a2.status == "nullified"
