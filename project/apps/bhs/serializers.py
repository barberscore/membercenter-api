
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from django.contrib.auth import get_user_model

# Local
from .fields import TimezoneField
from .models import Group
from .models import Member
from .models import Officer
from .models import Person

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    included_serializers = {
        # 'repertories': 'apps.bhs.serializers.RepertorySerializer',
        # 'members': 'apps.bhs.serializers.MemberSerializer',
        # 'officers': 'apps.bhs.serializers.OfficerSerializer',
    }

    class Meta:
        model = Group
        fields = [
            'id',
            'name',
            'status',
            'kind',
            'gender',
            'representing',
            'division',
            'bhs_id',
            'code',
            'website',
            'email',
            'phone',
            'fax_phone',
            'start_date',
            'end_date',
            'location',
            'facebook',
            'twitter',
            'youtube',
            'pinterest',
            'flickr',
            'instagram',
            'soundcloud',
            'image',
            'description',
            'visitor_information',
            'participants',
            'chapters',
            'notes',
            'tree_sort',

            'is_senior',
            'is_youth',
            'is_divided',

            'owners',
            'parent',
            # 'children',

            # 'repertories',
            'permissions',
            'usernames',

            'nomen',
            'image_id',
            'created',
            'modified',
        ]

        read_only_fields = [
            'nomen',
            'usernames',
            'image_id',
            'created',
            'modified',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'repertories',
            # 'members',
            # 'officers',
        ]

    # def to_representation(self, instance):
    #     if instance.kind <= 30:
    #         self.fields.pop('members')
    #     return super().to_representation(instance)


class MemberSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Member
        fields = [
            'id',
            'status',
            'part',
            'start_date',
            'end_date',
            'group',
            'person',
            'permissions',
        ]


class OfficerSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Officer
        fields = [
            'id',
            'status',
            'start_date',
            'end_date',
            'office',
            'person',
            'group',
            'permissions',
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=Officer.objects.all(),
                fields=('person', 'office'),
                message='This person already holds this office.',
            )
        ]


class PersonSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    # owners = ResourceRelatedField(
    #     queryset=User.objects,
    #     many=True,
    #     read_only=False,
    #     related_link_lookup_field='username',
    # )
    # included_serializers = {
    #     'owners': 'rest_framework_jwt.serializers.UserSerializer',
    #     # 'members': 'apps.bhs.serializers.MemberSerializer',
    #     # 'officers': 'apps.bhs.serializers.OfficerSerializer',
    # }

    class Meta:
        model = Person
        fields = [
            'id',
            'status',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'suffix',
            'birth_date',
            'spouse',
            'location',
            'part',
            'mon',
            'gender',
            'representing',
            'is_deceased',
            'is_honorary',
            'is_suspended',
            'is_expelled',
            'website',
            'email',
            'address',
            'home_phone',
            'work_phone',
            'cell_phone',
            'airports',
            'image',
            'description',
            'notes',
            'bhs_id',

            'nomen',
            'name',
            'full_name',
            'common_name',
            'sort_name',
            'initials',
            'image_id',
            # 'current_through',
            # 'current_status',
            # 'current_district',

            'usernames',
            'permissions',
            'created',
            'modified',
        ]
        read_only_fields = [
            'nomen',
            'name',
            'full_name',
            'common_name',
            'sort_name',
            'initials',
            'image_id',
            'usernames',
            # 'current_through',
            # 'current_status',
            # 'current_district',
            'created',
            'modified',
        ]
    class JSONAPIMeta:
        included_resources = [
            # 'owners',
            # 'members',
            # 'officers',
        ]