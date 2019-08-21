
# Third-Party
import pytest
from rest_framework import status

# Django
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_group_endpoint(admin_api_client, group, django_assert_max_num_queries):
    with django_assert_max_num_queries(14):
        path = reverse('group-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(14):
        path = reverse('group-detail', args=(str(group.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK


def test_person_endpoint(admin_api_client, person, django_assert_max_num_queries):
    with django_assert_max_num_queries(10):
        path = reverse('person-list')
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
    with django_assert_max_num_queries(10):
        path = reverse('person-detail', args=(str(person.id),))
        response = admin_api_client.get(path)
        assert response.status_code == status.HTTP_200_OK
