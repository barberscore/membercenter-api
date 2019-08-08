
# Django
from django.contrib import admin

# Local
from .models import Group
from .models import Member
from .models import Officer


class MemberInline(admin.TabularInline):
    model = Member
    fields = [
        'person',
        'group',
        'part',
        'start_date',
        'end_date',
        'status',
    ]
    autocomplete_fields = [
        'person',
        'group',
    ]
    ordering = (
        '-status',
        'part',
        'person__last_name',
        'person__first_name',
    )
    readonly_fields = [
        'status',
    ]

    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]


class OfficerInline(admin.TabularInline):
    model = Officer
    fields = [
        'office',
        'person',
        'group',
        'status',
    ]
    autocomplete_fields = [
        'person',
        'group',
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    ordering = [
        'person__last_name',
        'person__first_name',
    ]
    readonly_fields = [
        'status',
    ]


class ActiveChapterInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'parent',
        'code',
        # 'kind',
        'gender',
        # 'bhs_id',
        # 'status',
    ]
    fk_name = 'parent'
    ordering = [
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    verbose_name_plural = 'Active Chapters'

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries."""
        qs = super().get_queryset(request)
        qs = qs.filter(
            status__gt=0,
            kind=Group.KIND.chapter,
        )
        return qs


class ActiveChorusInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'parent',
        'bhs_id',
        # 'code',
        # 'kind',
        'gender',
        'status',
    ]
    fk_name = 'parent'
    ordering = [
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    verbose_name_plural = 'All Choruses'
    readonly_fields = [
        'status',
    ]

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries."""
        qs = super().get_queryset(request)
        qs = qs.filter(
            kind=Group.KIND.chorus,
        )
        return qs


class ActiveQuartetInline(admin.TabularInline):
    model = Group
    fields = [
        'name',
        'parent',
        'bhs_id',
        'is_senior',
        'is_youth',
        'gender',
        # 'status',
    ]
    fk_name = 'parent'
    ordering = [
    ]
    show_change_link = True
    extra = 0
    classes = [
        'collapse',
    ]
    verbose_name_plural = 'Active Quartets'
    readonly_fields = [
        'status',
    ]

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries."""
        qs = super().get_queryset(request)
        qs = qs.filter(
            status__gt=0,
            kind=Group.KIND.quartet,
        )
        return qs
