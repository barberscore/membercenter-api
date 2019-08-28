from rest_framework_json_api import views

from .filtersets import GroupFilterset
from .filtersets import PersonFilterset
from .models import Group
from .models import Person

from .serializers import GroupSerializer
from .serializers import PersonSerializer


class GroupViewSet(views.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_class = GroupFilterset
    ordering_fields = '__all__'
    ordering = [
        'id',
    ]
    resource_name = "group"


class PersonViewSet(views.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    filterset_class = PersonFilterset
    ordering_fields = '__all__'
    ordering = [
        'id',
    ]
    resource_name = "person"
