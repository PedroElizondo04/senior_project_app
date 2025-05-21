import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def admin_user(db):
    user = User.objects.create_superuser(username='admin', email='admin@example.com', password='testpass123')
    return user

@pytest.mark.django_db
def test_admin_login(client, admin_user):
    response = client.post(reverse('login'), {'username': 'admin', 'password': 'testpass123'})
    assert response.status_code == 302
    assert response.url == reverse('admin_landing')

@pytest.mark.django_db
def test_admin_landing_navigation(client, admin_user):
    client.login(username='admin', password='testpass123')
    landing_response = client.get(reverse('admin_landing'))
    assert landing_response.status_code == 200

    projects_response = client.get(reverse('project_list'))
    assert projects_response.status_code == 200

    students_response = client.get(reverse('student_list'))
    assert students_response.status_code == 200

    advisors_response = client.get(reverse('advisor_list'))
    assert advisors_response.status_code == 200