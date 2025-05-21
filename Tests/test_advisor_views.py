import pytest
from django.urls import reverse
from django.contrib.auth.models import User

@pytest.fixture
def advisor_user(db):
    user = User.objects.create_user(username='advisor', email='advisor@example.com', password='testpass123')
    return user

@pytest.mark.django_db
def test_advisor_login(client, advisor_user):
    response = client.post(reverse('login'), {'username': 'advisor', 'password': 'testpass123'})
    assert response.status_code == 302
    assert response.url == reverse('advisor_landing')

@pytest.mark.django_db
def test_advisor_landing_navigation(client, advisor_user):
    client.login(username='advisor', password='testpass123')
    landing_response = client.get(reverse('advisor_landing'))
    assert landing_response.status_code == 200

    my_groups_response = client.get(reverse('my_groups'))
    assert my_groups_response.status_code == 200

    view_projects_response = client.get(reverse('project_list'))
    assert view_projects_response.status_code == 200

    view_students_response = client.get(reverse('student_list'))
    assert view_students_response.status_code == 200