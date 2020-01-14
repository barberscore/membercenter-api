# Django
from django.contrib import admin

# Local
from .inlines import JoinInline
from .inlines import RoleInline
from .inlines import StructureInline
from .inlines import SubscriptionInline
from .models import Address
from .models import Human
from .models import Join
from .models import Membership
from .models import Role
from .models import Status
from .models import Structure
from .models import Subscription


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


@admin.register(Human)
class HumanAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'username',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        'birth_date',
        'is_deceased',
        'created',
        'created_by',
        'modified',
        'modified_by',
        'deleted',
        'deleted_by',
        'home_phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'gender',
        'part',
        'is_honorary',
        'is_suspended',
        'merged_id',
        'mon',
        'is_expelled',
    ]

    list_display = [
        '__str__',
        # 'first_name',
        # 'middle_name',
        # 'last_name',
        # 'nick_name',
        'email',
        'home_phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'birth_date',
        'gender',
        'part',
        'created',
        'modified',
    ]

    readonly_fields = [
        'id',
        'username',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        'birth_date',
        'is_deceased',
        'created',
        'created_by',
        'modified',
        'modified_by',
        'deleted',
        'deleted_by',
        'home_phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'gender',
        'part',
        'is_honorary',
        'is_suspended',
        'merged_id',
        'mon',
        'is_expelled',
    ]

    list_filter = [
        'gender',
        'part',
        'is_deceased',
        'is_honorary',
        'is_suspended',
        'is_expelled',
        'created',
        'modified',
    ]

    search_fields = [
        'first_name',
        'last_name',
        'bhs_id',
        'email',
    ]

    inlines = [
        RoleInline,
        SubscriptionInline,
    ]

    ordering = [
        'last_name',
        'first_name',
    ]


@admin.register(Structure)
class StructureAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'name',
        'kind',
        'gender',
        'county',
        'country',
        'bhs_id',
        'chapter_code',
        'chorus_name',
        'website',
        'tin',
        'established_date',
        'visitor_information',
        'created',
        'created_by',
        'modified',
        'modified_by',
        'deleted',
        'deleted_by',
        'phone',
        'phone_ext',
        'fax',
        'email',
        'facebook',
        'twitter',
        'youtube',
        'pinterest',
        'flickr',
        'instagram',
        'soundcloud',
        'preferred_name',
        'first_alternate_name',
        'second_alternate_name',
        'is_default',
        'parent',
        'division',
        'status',
        'licenced_date',
        'chartered_date',
        'lft',
        'rght',
    ]

    list_display = [
        '__str__',
        'name',
        'kind',
        'gender',
        'bhs_id',
        'preferred_name',
        'chapter_code',
        'phone',
        'email',
        'established_date',
        'status',
        'parent',
        'created',
        'modified',
    ]

    readonly_fields = [
        'id',
        'name',
        'kind',
        'gender',
        'county',
        'country',
        'bhs_id',
        'chapter_code',
        'chorus_name',
        'website',
        'tin',
        'established_date',
        'visitor_information',
        'created',
        'created_by',
        'modified',
        'modified_by',
        'deleted',
        'deleted_by',
        'phone',
        'phone_ext',
        'fax',
        'email',
        'facebook',
        'twitter',
        'youtube',
        'pinterest',
        'flickr',
        'instagram',
        'soundcloud',
        'preferred_name',
        'first_alternate_name',
        'second_alternate_name',
        'is_default',
        'parent',
        'division',
        'status',
        'licenced_date',
        'chartered_date',
        'lft',
        'rght',
    ]

    list_filter = [
        'kind',
        'gender',
        'division',
    ]
    search_fields = [
        'name',
        'bhs_id',
        'chapter_code',
    ]

    list_select_related = [
        'parent',
        'status',
    ]

    ordering = (
        '-created',
    )

    INLINES = {
        'organization': [
            RoleInline,
        ],
        'district': [
            RoleInline,
        ],
        'group': [
            RoleInline,
        ],
        'chapter': [
            RoleInline,
            StructureInline,
        ],
        'chorus': [
            RoleInline,
        ],
        'quartet': [
            RoleInline,
            JoinInline,
        ],
    }

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        inlines = self.INLINES[obj.kind]
        # try:
        #     inlines = self.INLINES[obj.kind]
        # except AttributeError:
        #     return inline_instances
        # except KeyError:
        #     # Defaults to Group
        #     inlines = self.INLINES['Group']

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            inline_instances.append(inline)
        return inline_instances

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)


@admin.register(Status)
class StatusAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'name',
        'label',
        'non_admin_view',
        'non_admin_join',
        'renewable',
        'entities',
    ]
    readonly_fields = [
        'id',
        'name',
        'label',
        'non_admin_view',
        'non_admin_join',
        'renewable',
        'entities',
    ]


@admin.register(Membership)
class MembershipAdmin(ReadOnlyAdmin):
    fields = [
        'object_type',
        'structure',
        'months',
        'is_auto_renew',
        'type',
        'code',
        'membership_options_id',
        'effective_date',
        'created',
        'created_by',
        'deleted',
        'deleted_by',
        'modified',
        'status',
    ]

    list_display = [
        'structure',
        'code',
        'status',
        'created',
        'modified',
    ]

    list_select_related = [
        'structure',
    ]

    list_filter = [
        'structure__kind',
        'code',
        'status',
    ]

    readonly_fields = [
        'object_type',
        'structure',
        'months',
        'is_auto_renew',
        'type',
        'code',
        'membership_options_id',
        'effective_date',
        'created',
        'created_by',
        'deleted',
        'deleted_by',
        'modified',
        'status',
    ]

    inlines = [
        JoinInline,
    ]

    ordering = (
        'structure__name',
        'code',
    )

    search_fields = [
        'structure__name',
    ]


@admin.register(Subscription)
class SubscriptionAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'members_entities_id',
        'modified',
        'current_through',
        'memberships_id',
        'created',
        'status',
        'human',
        'join_date',
        'items_editable',
        'deleted',
    ]

    list_display = [
        '__str__',
        'items_editable',
        'current_through',
        'status',
        'created',
        'modified',
    ]

    fields = [
        'id',
        'members_entities_id',
        'modified',
        'current_through',
        'memberships_id',
        'created',
        'status',
        'human',
        'join_date',
        'items_editable',
        'deleted',
    ]

    list_filter = [
        'status',
    ]
    search_fields = (
        'human__last_name',
        'human__first_name',
        'human__bhs_id',
    )

    ordering = (
        'human__last_name',
    )

    inlines = [
        JoinInline,
    ]


@admin.register(Role)
class RoleAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'object_type',
        'structure',
        'officer_roles_id',
        'name',
        'abbv',
        'start_date',
        'end_date',
        'human',
        'created',
        'modified',
    ]

    list_display = [
        'name',
        'human',
        'structure',
        'start_date',
        'end_date',
        'abbv',
        'created',
        'modified',
    ]

    list_select_related = [
        'structure',
        'human',
    ]
    list_filter = [
        'name',
    ]

    readonly_fields = [
        'id',
        'object_type',
        'structure',
        'officer_roles_id',
        'name',
        'abbv',
        'start_date',
        'end_date',
        'human',
        'created',
        'modified',
    ]


    ordering = (
        'structure__name',
    )

    search_fields = [
        'structure__name',
        'human__first_name',
        'human__last_name',
        'human__bhs_id',
    ]


@admin.register(Join)
class JoinAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'subscription',
        'membership',
        'status',
        'established_date',
        'inactive_date',
        'inactive_reason',
        'paid',
        'part',
        'structure',
        'modified',
        'created',
        'deleted',
    ]

    list_display = [
        'id',
        'status',
        'paid',
        'subscription',
        'membership',
        'part',
        'inactive_date',
        'inactive_reason',
        'established_date',
        'created',
        'modified',
    ]

    list_select_related = [
        'subscription',
        'membership',
    ]
    readonly_fields = [
        'id',
        'subscription',
        'membership',
        'status',
        'established_date',
        'inactive_date',
        'inactive_reason',
        'paid',
        'part',
        'structure',
        'modified',
        'created',
        'deleted',
    ]

    list_display_links = [
        'id',
    ]

    list_filter = [
        'status',
        'paid',
        'part',
        'structure__kind',
        'inactive_date',
    ]

    search_fields = [
        'subscription__human__last_name',
        'subscription__human__bhs_id',
        # 'membership__structure__name',
        # 'membership__structure__bhs_id',
    ]


@admin.register(Address)
class AddressAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'name',
        'object_type',
        'object_id',
        'kind',
        'city',
        'state',
        'country',
        'status',
        'modified',
        'created',
        'lat',
        'lon',
        'legacy_id',
        'deleted',
    ]

    list_display = [
        'id',
        'name',
        'object_type',
        'object_id',
        'kind',
        'city',
        'state',
        'country',
        'status',
        'modified',
        'created',
        'lat',
        'lon',
        'legacy_id',
        'deleted',
    ]

    list_select_related = [
        # 'subscription',
        # 'membership',
    ]
    readonly_fields = [
        'id',
        'name',
        'object_type',
        'object_id',
        'kind',
        'city',
        'state',
        'country',
        'status',
        'modified',
        'created',
        'lat',
        'lon',
        'legacy_id',
        'deleted',
    ]

    list_display_links = [
        # 'id',
    ]

    list_filter = [
        'object_type',
        'kind',
        'status',
    ]

    search_fields = [
        # 'subscription__human__last_name',
        # 'subscription__human__bhs_id',
        # 'membership__structure__name',
        # 'membership__structure__bhs_id',
    ]
