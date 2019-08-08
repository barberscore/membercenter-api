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
        ('first_name', 'middle_name', 'last_name', 'nick_name',),
        ('email', 'bhs_id', 'birth_date',),
        ('home_phone', 'work_phone', 'cell_phone',),
        ('part', 'gender',),
        ('is_deceased', 'is_honorary', 'is_suspended', 'is_expelled',),
        ('merged_id', 'deleted_id',),
        ('created', 'modified',),
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
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        'home_phone',
        'cell_phone',
        'work_phone',
        'bhs_id',
        'birth_date',
        'gender',
        'part',
        'mon',
        'is_deceased',
        'is_honorary',
        'is_suspended',
        'is_expelled',
        'created',
        'modified',
    ]

    list_filter = [
        'gender',
        'part',
        'is_deceased',
        'is_honorary',
        'is_suspended',
        'is_expelled',
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

    ordering = (
        'last_name',
        'first_name',
    )


@admin.register(Structure)
class StructureAdmin(ReadOnlyAdmin):
    fields = [
        'id',
        'name',
        'kind',
        'gender',
        'division',
        'bhs_id',
        'preferred_name',
        'chapter_code',
        'phone',
        'email',
        'website',
        'facebook',
        'twitter',
        'established_date',
        'status',
        'parent',
        'created',
        'modified',
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
        'division',
        'bhs_id',
        'preferred_name',
        'chapter_code',
        'phone',
        'email',
        'website',
        'facebook',
        'twitter',
        'established_date',
        'status',
        'parent',
        'created',
        'modified',
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


@admin.register(Membership)
class MembershipAdmin(ReadOnlyAdmin):
    fields = [
        'structure',
        'code',
        'status',
        'created',
        'modified',
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
        'structure',
        'code',
        'status',
        'created',
        'modified',
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
        '__str__',
        'items_editable',
        'current_through',
        'status',
        'created',
        'modified',
    ]

    list_display = [
        '__str__',
        'items_editable',
        'current_through',
        'status',
        'created',
        'modified',
    ]

    readonly_fields = [
        '__str__',
        'items_editable',
        'current_through',
        'status',
        'created',
        'modified',
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
        'name',
        'human',
        'structure',
        'start_date',
        'end_date',
        'abbv',
        'officer_roles_id',
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
        'name',
        'human',
        'structure',
        'start_date',
        'end_date',
        'abbv',
        'officer_roles_id',
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
        'status',
        'paid',
        'part',
        'subscription',
        'membership',
        'established_date',
        'inactive_date',
        'inactive_reason',
        'created',
        'modified',
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
        'updated',
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
        'updated',
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
        'updated',
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
