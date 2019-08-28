# Third-Party
from django_filters.rest_framework import FilterSet

# Local
from .models import Group
from .models import Person


class GroupFilterset(FilterSet):
    class Meta:
        model = Group
        fields = {
            'status': [
                'exact',
            ],
            'kind': [
                'gt',
            ],
            'modified': [
                'gt',
            ],
        }


class PersonFilterset(FilterSet):
    class Meta:
        model = Person
        fields = {
            'status': [
                'exact',
            ],
            'modified': [
                'gt',
            ],
        }
