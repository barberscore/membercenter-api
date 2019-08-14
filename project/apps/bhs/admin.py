# Third-Party
from django_fsm_log.admin import StateLogInline
from fsm_admin.mixins import FSMTransitionMixin
from reversion.admin import VersionAdmin

# Django
from django.contrib import admin

# Local
from .inlines import MemberInline
from .inlines import OfficerInline
from .models import Group
from .models import Member
from .models import Officer
from .models import Person

admin.site.disable_action('delete_selected')


@admin.register(Group)
class GroupAdmin(VersionAdmin, FSMTransitionMixin):
    save_on_top = True
    fsm_field = [
        'status',
    ]
    fields = [
        'id',
        'name',
        'status',
        'kind',
        'gender',
        'representing',
        'division',
        'owners',
        ('is_senior', 'is_youth',),
        ('bhs_id', 'code',),
        'parent',
        'location',
        'email',
        'phone',
        'website',
        'image',
        'description',
        'participants',
        'chapters',
        'notes',
        ('created', 'modified',),
    ]

    list_filter = [
        'status',
        'kind',
        'gender',
        'is_senior',
        'is_youth',
        'representing',
        'division',
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
        'is_senior',
        'is_youth',
        'representing',
        'division',
        'parent',
        'bhs_id',
        'code',
        'status',
    ]
    list_select_related = [
        'parent',
    ]
    readonly_fields = [
        'id',
        'created',
        'modified',
    ]

    autocomplete_fields = [
        'owners',
        # 'parent',
    ]
    raw_id_fields = [
        'parent',
    ]

    ordering = [
        'tree_sort',
    ]

    INLINES = {
        'International': [
            # AwardInline,
            # OfficerInline,
            # ConventionInline,
            StateLogInline,
        ],
        'District': [
            # AwardInline,
            # OfficerInline,
            # ConventionInline,
            # ActiveChapterInline,
            # ActiveQuartetInline,
            StateLogInline,
        ],
        'Noncompetitive': [
            # OfficerInline,
            # GroupInline,
            StateLogInline,
        ],
        'Affiliate': [
            # OfficerInline,
            # GroupInline,
            StateLogInline,
        ],
        'Chapter': [
            # ActiveChorusInline,
            # OfficerInline,
            StateLogInline,
        ],
        'Chorus': [
            OfficerInline,
            # MemberInline,
            # EntryInline,
            StateLogInline,
        ],
        'Quartet': [
            # MemberInline,
            OfficerInline,
            # EntryInline,
            StateLogInline,
        ],
        'VLQ': [
            # MemberInline,
            OfficerInline,
            # EntryInline,
            StateLogInline,
        ],
    }

    def get_inline_instances(self, request, obj=None):
        inline_instances = []
        try:
            inlines = self.INLINES[obj.KIND[obj.kind]]
        except AttributeError:
            return inline_instances

        for inline_class in inlines:
            inline = inline_class(self.model, self.admin_site)
            inline_instances.append(inline)
        return inline_instances

    def get_formsets(self, request, obj=None):
        for inline in self.get_inline_instances(request, obj):
            yield inline.get_formset(request, obj)

    def get_queryset(self, request):
        return super().get_queryset(
            request
        ).prefetch_related('members')


@admin.register(Member)
class MemberAdmin(VersionAdmin, FSMTransitionMixin):
    fsm_field = [
        'status',
    ]
    fields = [
        'id',
        'status',
        'person',
        'group',
        'part',
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
        'created',
        'modified',
    ]
    list_display = [
        'person',
        'group',
        'part',
        'status',
    ]
    readonly_fields = [
        'id',
        'part',
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
        'created',
        'modified',
    ]

    autocomplete_fields = [
        'person',
        'group',
    ]
    search_fields = [
        'person__first_name',
        'person__last_name',
        'group__name',
        'person__bhs_id',
        'group__bhs_id',
    ]
    list_filter = [
        'status',
        'group__kind',
        'group__status',
        'part',
        'start_date',
        'end_date',
        # 'inactive_date',
        # 'inactive_reason',
        # 'sub_status',
        # 'mem_code',
        # 'mem_status',
        'created',
    ]
    list_select_related = [
        'person',
        'group',
    ]
    inlines = [
        StateLogInline,
    ]


@admin.register(Officer)
class OfficerAdmin(VersionAdmin, FSMTransitionMixin):
    fsm_field = [
        'status',
    ]

    fields = [
        'id',
        'status',
        'person',
        'office',
        'group',
        'start_date',
        'end_date',
    ]

    list_display = [
        'person',
        'office',
        'group',
        'status',
    ]
    readonly_fields = [
        'id',
    ]
    list_select_related = [
        'person',
        'group',
    ]
    list_filter = [
        'status',
        'group__kind',
        'office',
    ]
    inlines = [
        StateLogInline,
    ]
    search_fields = [
        'person__last_name',
        'group__name',
    ]
    autocomplete_fields = [
        'person',
        'group',
    ]
    ordering = [
        'office',
        'person__last_name',
        'person__first_name',
    ]


@admin.register(Person)
class PersonAdmin(VersionAdmin, FSMTransitionMixin):
    fields = [
        'id',
        'status',
        ('first_name', 'middle_name', 'last_name', 'nick_name',),
        ('email', 'bhs_id', 'birth_date',),
        ('home_phone', 'work_phone', 'cell_phone',),
        ('part', 'gender',),
        'current_through',
        ('is_deceased', 'is_honorary', 'is_suspended', 'is_expelled',),
        'spouse',
        'location',
        'representing',
        'website',
        'image',
        'description',
        'notes',
        'owners',
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
    ]

    raw_id_fields = [
        # 'user',
    ]

    readonly_fields = [
        'id',
        'first_name',
        'middle_name',
        'last_name',
        'nick_name',
        'email',
        'current_through',
        'is_deceased',
        'bhs_id',
        'birth_date',
        'part',
        'mon',
        'gender',
        'home_phone',
        'work_phone',
        'cell_phone',
        'common_name',
        'is_deceased',
        'is_honorary',
        'is_suspended',
        'is_expelled',
        'created',
        'modified',
    ]

    fsm_field = [
        'status',
    ]

    search_fields = [
        'last_name',
        'first_name',
        'nick_name',
        'bhs_id',
        'email',
    ]

    autocomplete_fields = [
        'owners',
    ]

    save_on_top = True

    inlines = [
        # MemberInline,
        OfficerInline,
        # AssignmentInline,
        # PanelistInline,
        StateLogInline,
    ]

    ordering = [
        'last_name',
        'first_name',
    ]
    # readonly_fields = [
    #     'common_name',
    # ]
