
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db



def test_group_endpoint(anon_api_client, group):
    path = reverse('group-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('group-detail', args=(str(group.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_person_endpoint(anon_api_client, person):
    path = reverse('person-list')
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.post(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    path = reverse('person-detail', args=(str(person.id),))
    response = anon_api_client.get(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.patch(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = anon_api_client.delete(path)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
