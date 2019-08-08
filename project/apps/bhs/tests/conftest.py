
# Third-Party
import pytest
from rest_framework.test import APIClient

# Django
from django.test.client import Client

# Local
from .factories import AwardFactory
from .factories import ChartFactory
from .factories import ConventionFactory
from .factories import GroupFactory
from .factories import PersonFactory
from .factories import UserFactory


@pytest.fixture
def admin_django_client():
    admin = UserFactory(
        is_staff=True,
    )
    client = Client()
    client.force_login(admin)
    return client


@pytest.fixture
def admin_api_client():
    admin = UserFactory(
        is_staff=True,
    )
    client = APIClient()
    client.force_authenticate(user=admin)
    return client


@pytest.fixture
def user_api_client():
    # person = PersonFactory()
    user = UserFactory(
        is_staff=False,
        # person=person,
    )
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def anon_api_client():
    client = APIClient()
    return client


@pytest.fixture
def award():
    return AwardFactory()


@pytest.fixture
def chart():
    return ChartFactory()


@pytest.fixture
def convention():
    return ConventionFactory()


@pytest.fixture
def group():
    return GroupFactory()



@pytest.fixture
def person():
    return PersonFactory()


@pytest.fixture
def user():
    return UserFactory()
