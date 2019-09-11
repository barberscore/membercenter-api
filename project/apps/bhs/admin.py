# Django
from django.contrib import admin

# Local
from .models import Group
from .models import Person

from django_object_actions import DjangoObjectActions
from rest_framework_jwt.models import User
from rest_framework_jwt.models import Role
from rest_framework.authtoken.models import Token

from django.apps import apps


admin.site.unregister(User)
admin.site.unregister(Role)
admin.site.unregister(Token)

admin.site.disable_action('delete_selected')

class ReadOnlyAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super().changeform_view(request, object_id, extra_context=extra_context)


@admin.register(Group)
class GroupAdmin(DjangoObjectActions, ReadOnlyAdmin):
    save_on_top = True
    fields = [
        'id',
        'name',
        'status',
        'kind', 'gender',
        'district', 'division',
        'bhs_id', 'code',
        'owners',
        # 'parent',
        # 'location',
        # 'email',
        # 'phone',
        # 'website',
        ('created', 'modified',),
    ]

    list_filter = [
        'status',
        'kind',
        'gender',
        'district',
        'division',
        'modified',
        'created',
    ]

    search_fields = [
        'name',
        'bhs_id',
        'code',
    ]

    list_display = [
        'name',
        'kind',
        'gender',
        'district',
        'division',
        'bhs_id',
        'code',
        'status',
    ]
    readonly_fields = [
        'id',
        'name',
        'status',
        'kind',
        'gender',
        'district',
        'division',
        'bhs_id',
        'code',
        'website',
        'email',
        'phone',
        'fax_phone',
        'start_date',
        'end_date',
        'facebook',
        'twitter',
        'youtube',
        'pinterest',
        'flickr',
        'instagram',
        'soundcloud',
        'visitor_information',
        'owners',
        'parent',
        'created',
        'modified',
    ]

    ordering = [
        'tree_sort',
    ]

    def update_from_source(self, request, obj):
        Structure = apps.get_model('source.structure')
        structure = Structure.objects.export_values(pk=obj.id)[0]
        return Group.objects.update_or_create_from_structure(structure)
    update_from_source.label = "Update"
    update_from_source.short_description = "Update from Source Database"

    change_actions = ('update_from_source', )


@admin.register(Person)
class PersonAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'status',
        'current_through',
        'first_name', 'middle_name', 'last_name', 'nick_name',
        'email', 'bhs_id', 'birth_date',
        'home_phone', 'work_phone', 'cell_phone',
        'part', 'gender',
        ('is_deceased', 'is_honorary', 'is_suspended', 'is_expelled',),
        # 'spouse',
        # 'location',
        # 'image',
        # 'description',
        # 'notes',
        # 'owners',
        ('created', 'modified',),
        # 'user',
    ]

    list_display = [
        'common_name',
        'email',
        'cell_phone',
        'part',
        'gender',
        'status',
    ]

    list_filter = [
        'status',
        'current_through',
        'gender',
        'part',
        'is_deceased',
        'created',
        'modified',
    ]

    raw_id_fields = [
        # 'user',
    ]

    readonly_fields = [
        'id',
        'status',
        'prefix',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'suffix',
        'birth_date',
        'part',
        'mon',
        'gender',
        'is_deceased',
        'is_honorary',
        'is_suspended',
        'is_expelled',
        'email',
        'address',
        'home_phone',
        'work_phone',
        'cell_phone',
        'bhs_id',
        'current_through',
        'created',
        'modified',
        'owners',
    ]

    search_fields = [
        'last_name',
        'first_name',
        'nick_name',
        'bhs_id',
        'email',
    ]

    autocomplete_fields = [
        # 'owners',
    ]

    save_on_top = True

    inlines = [
        # MemberInline,
        # OfficerInline,
        # AssignmentInline,
        # PanelistInline,
        # StateLogInline,
    ]

    ordering = [
        'last_name',
        'first_name',
    ]
