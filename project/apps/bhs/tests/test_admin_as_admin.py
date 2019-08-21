
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_api_admin(admin_django_client):
    path = reverse('admin:index')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_group_admin(admin_django_client, group):
    path = reverse('admin:bhs_group_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:bhs_group_change', args=(str(group.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_admin(admin_django_client, person):
    path = reverse('admin:bhs_person_changelist')
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('admin:bhs_person_change', args=(str(person.id),))
    response = admin_django_client.get(path)
    assert response.status_code == status.HTTP_200_OK
