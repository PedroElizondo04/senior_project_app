import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from projects.models import Student

@pytest.mark.django_db
def test_login_happy(client):
    User.objects.create_user(username="user", password="pass")
    response = client.post(reverse("login"), {"username": "user", "password": "pass"})
    assert response.status_code == 302  # Redirect to landing
    assert response.url == reverse("landing")

@pytest.mark.django_db
def test_login_sad(client):
    response = client.post(reverse("login"), {"username": "bad", "password": "wrong"})
    assert b"Invalid email or password." in response.content

@pytest.mark.django_db
def test_student_cannot_view_student_list(client):
    u = User.objects.create_user("stu", password="pass")
    Student.objects.create(user=u)
    client.force_login(u)
    response = client.get(reverse("studentList"))
    assert response.status_code == 403
