
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_group_endpoint(user_api_client, group):
    path = reverse('group-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('group-detail', args=(str(group.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK


def test_person_endpoint(user_api_client, person):
    path = reverse('person-list')
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
    path = reverse('person-detail', args=(str(person.id),))
    response = user_api_client.get(path)
    assert response.status_code == status.HTTP_200_OK
