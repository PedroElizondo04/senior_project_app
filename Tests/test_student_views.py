import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def student_user(db):
    user = User.objects.create_user(username='student', email='student@example.com', password='testpass123')
    return user

@pytest.mark.django_db
def test_student_login(client, student_user):
    response = client.post(reverse('login'), {'username': 'student', 'password': 'testpass123'})
    assert response.status_code == 302
    assert response.url == reverse('student_landing')

@pytest.mark.django_db
def test_student_login_failure(client):
    response = client.post(reverse('login'), {'username': 'student', 'password': 'wrongpass'})
    assert response.status_code == 200
    assert 'error' in response.content.decode()

@pytest.mark.django_db
def test_student_landing_navigation(client, student_user):
    client.login(username='student', password='testpass123')
    landing_response = client.get(reverse('student_landing'))
    assert landing_response.status_code == 200

    create_project_response = client.get(reverse('create_project'))
    assert create_project_response.status_code == 200

    view_projects_response = client.get(reverse('project_list'))
    assert view_projects_response.status_code == 200

    view_advisors_response = client.get(reverse('advisor_list'))
    assert view_advisors_response.status_code == 200
