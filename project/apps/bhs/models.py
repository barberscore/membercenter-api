# Standard Library
import datetime
import uuid

# Third-Party
from django_fsm import FSMIntegerField
from django_fsm import transition
from django_fsm_log.decorators import fsm_log_by
from django_fsm_log.decorators import fsm_log_description
from django_fsm_log.models import StateLog
from dry_rest_permissions.generics import allow_staff_or_superuser
from dry_rest_permissions.generics import authenticated_users
from model_utils import Choices
from model_utils.models import TimeStampedModel
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from phonenumber_field.modelfields import PhoneNumberField

# Django
from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.postgres.fields import ArrayField
from django.core.files.base import ContentFile
from django.db import models
from django.utils.functional import cached_property
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Local
from .fields import ImageUploadPath
from .managers import MemberManager
from .managers import GroupManager
from .managers import OfficerManager
from .managers import PersonManager


class Group(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    name = models.CharField(
        max_length=255,
        default='UNKNOWN',
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (-5, 'aic', 'AIC',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        choices=STATUS,
        default=STATUS.new,
        editable=False,
    )

    KIND = Choices(
        ('International', [
            (1, 'international', "International"),
        ]),
        ('District', [
            (11, 'district', "District"),
            (12, 'noncomp', "Noncompetitive"),
        ]),
        ('Chapter', [
            (30, 'chapter', "Chapter"),
        ]),
        ('Group', [
            (32, 'chorus', "Chorus"),
            (41, 'quartet', "Quartet"),
        ]),
    )

    kind = models.IntegerField(
        choices=KIND,
        editable=False,
    )

    GENDER = Choices(
        (10, 'male', "Male"),
        (20, 'female', "Female"),
        (30, 'mixed', "Mixed"),
    )

    gender = models.IntegerField(
        choices=GENDER,
        editable=False,
    )

    DISTRICT = Choices(
        (110, 'bhs', 'BHS'),
        (200, 'car', 'CAR'),
        (205, 'csd', 'CSD'),
        (210, 'dix', 'DIX'),
        (215, 'evg', 'EVG'),
        (220, 'fwd', 'FWD'),
        (225, 'ill', 'ILL'),
        (230, 'jad', 'JAD'),
        (235, 'lol', 'LOL'),
        (240, 'mad', 'MAD'),
        (345, 'ned', 'NED'),
        (350, 'nsc', 'NSC'),
        (355, 'ont', 'ONT'),
        (360, 'pio', 'PIO'),
        (365, 'rmd', 'RMD'),
        (370, 'sld', 'SLD'),
        (375, 'sun', 'SUN'),
        (380, 'swd', 'SWD'),
    )

    district = models.IntegerField(
        choices=DISTRICT,
        blank=True,
        null=True,
        editable=False,
    )

    DIVISION = Choices(
        ('EVG', [
            (10, 'evgd1', 'EVG Division I'),
            (20, 'evgd2', 'EVG Division II'),
            (30, 'evgd3', 'EVG Division III'),
            (40, 'evgd4', 'EVG Division IV'),
            (50, 'evgd5', 'EVG Division V'),
        ]),
        ('FWD', [
            (60, 'fwdaz', 'FWD Arizona'),
            (70, 'fwdne', 'FWD Northeast'),
            (80, 'fwdnw', 'FWD Northwest'),
            (90, 'fwdse', 'FWD Southeast'),
            (100, 'fwdsw', 'FWD Southwest'),
        ]),
        ('LOL', [
            (110, 'lol10l', 'LOL 10000 Lakes'),
            (120, 'lolone', 'LOL Division One'),
            (130, 'lolnp', 'LOL Northern Plains'),
            (140, 'lolpkr', 'LOL Packerland'),
            (150, 'lolsw', 'LOL Southwest'),
        ]),
        ('MAD', [
            # (160, 'madatl', 'MAD Atlantic'),
            (170, 'madcen', 'MAD Central'),
            (180, 'madnth', 'MAD Northern'),
            (190, 'madsth', 'MAD Southern'),
            # (200, 'madwst', 'MAD Western'),
        ]),
        ('NED', [
            (210, 'nedgp', 'NED Granite and Pine'),
            (220, 'nedmtn', 'NED Mountain'),
            (230, 'nedpat', 'NED Patriot'),
            (240, 'nedsun', 'NED Sunrise'),
            (250, 'nedyke', 'NED Yankee'),
        ]),
        ('SWD', [
            (260, 'swdne', 'SWD Northeast'),
            (270, 'swdnw', 'SWD Northwest'),
            (280, 'swdse', 'SWD Southeast'),
            (290, 'swdsw', 'SWD Southwest'),
        ]),
    )

    division = models.IntegerField(
        choices=DIVISION,
        blank=True,
        null=True,
        editable=False,
    )

    bhs_id = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    code = models.CharField(
        help_text="""
            Short-form chapter code.""",
        max_length=255,
        blank=True,
        default='',
        editable=False,
    )

    website = models.URLField(
        help_text="""
            The website URL of the resource.""",
        blank=True,
        default='',
        editable=False,
    )

    email = models.EmailField(
        help_text="""
            The contact email of the resource.""",
        null=True,
        blank=True,
        editable=False,
    )

    phone = PhoneNumberField(
        help_text="""
            The phone number of the resource.  Include country code.""",
        blank=True,
        default='',
        editable=False,
    )

    fax_phone = PhoneNumberField(
        help_text="""
            The fax number of the resource.  Include country code.""",
        blank=True,
        default='',
        editable=False,
    )

    start_date = models.DateField(
        blank=True,
        null=True,
        editable=False,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
        editable=False,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=255,
        blank=True,
        default='',
        editable=True,
    )

    facebook = models.URLField(
        help_text="""
            The facebook URL of the resource.""",
        blank=True,
        default='',
        editable=False,
    )

    twitter = models.URLField(
        help_text="""
            The twitter URL of the resource.""",
        blank=True,
        default='',
        editable=False,
    )

    youtube = models.URLField(
        help_text="""
            The youtube URL of the resource.""",
        blank=True,
        default='',
        editable=False,
    )

    pinterest = models.URLField(
        help_text="""
            The pinterest URL of the resource.""",
        blank=True,
        default='',
        editable=False,
    )

    flickr = models.URLField(
        help_text="""
            The flickr URL of the resource.""",
        blank=True,
        default='',
        editable=False,
    )

    instagram = models.URLField(
        help_text="""
            The instagram URL of the resource.""",
        blank=True,
        default='',
        editable=False,
    )

    soundcloud = models.URLField(
        help_text="""
            The soundcloud URL of the resource.""",
        blank=True,
        default='',
        editable=False,
    )

    image = models.ImageField(
        upload_to=ImageUploadPath('image'),
        blank=True,
        default='',
        editable=True,
    )

    description = models.TextField(
        help_text="""
            A description of the group.  Max 1000 characters.""",
        max_length=1000,
        blank=True,
        default='',
        editable=True,
    )

    visitor_information = models.TextField(
        max_length=255,
        blank=True,
        default='',
        editable=False,
    )

    participants = models.CharField(
        help_text='Director(s) or Members (listed TLBB)',
        max_length=255,
        blank=True,
        default='',
        editable=True,
    )

    chapters = models.CharField(
        help_text="""
            The denormalized chapter group.""",
        max_length=255,
        blank=True,
        default='',
        editable=True,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
        default='',
        editable=True,
    )

    is_senior = models.BooleanField(
        help_text="""Qualifies as a Senior Group.  Must be set manually.""",
        blank=True,
        default=False,
        editable=True,
    )

    is_youth = models.BooleanField(
        help_text="""Qualifies as a Youth Group.  Must be set manually.""",
        blank=True,
        default=False,
        editable=True,
    )

    # Group Denormalization
    tree_sort = models.IntegerField(
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )

    # Group FKs
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        help_text="""
            These are the active officers with active accounts.
        """,
        related_name='groups',
        blank=True,
        editable=False,
    )

    parent = models.ForeignKey(
        'Group',
        blank=True,
        null=True,
        related_name='children',
        db_index=True,
        on_delete=models.SET_NULL,
        editable=False,
    )

    # Group Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='groups',
    )

    # Group Properties
    @cached_property
    def nomen(self):
        if self.bhs_id:
            suffix = "[{0}]".format(self.bhs_id)
        else:
            suffix = "[No BHS ID]"
        if self.code:
            code = "({0})".format(self.code)
        else:
            code = ""
        full = [
            self.name,
            code,
            suffix,
        ]
        return " ".join(full)

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

    @cached_property
    def image_url(self):
        try:
            return self.image.url
        except ValueError:
            return 'https://res.cloudinary.com/barberscore/image/upload/v1554830585/missing_image.jpg'

    # Group Methods
    def update_owners(self):
        User = get_user_model()
        emails = self.officers.filter(
            person__email__isnull=False,
        ).values_list(
            'person__email',
            flat=True,
        )
        owners = User.objects.filter(
            email__in=emails,
        ).distinct()
        self.owners.set(owners)
        # the self.save is only necessary to touch the modified field.
        return self.save()

    def get_roster(self):
        Member = apps.get_model('bhs.member')
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'BHS ID',
            'First Name',
            'Last Name',
            'Expiration Date',
            'Status',
        ]
        ws.append(fieldnames)
        members = self.members.filter(
            status=Member.STATUS.active,
        ).order_by('person__last_name', 'person__first_name')
        for member in members:
            bhs_id = member.person.bhs_id
            first_name = member.person.first_name
            last_name = member.person.last_name
            expiration = member.person.current_through
            status = member.person.get_status_display()
            row = [
                bhs_id,
                first_name,
                last_name,
                expiration,
                status,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content

    # Algolia
    def is_active(self):
        return bool(self.status == self.STATUS.active)

    def owner_ids(self):
        return [str(owner.id) for owner in self.owners.all()]

    def get_officer_emails(self):
        officers = self.officers.filter(
            status__gt=0,
            person__email__isnull=False,
        ).order_by(
            'person__last_name',
            'person__first_name',
        )
        seen = set()
        result = [
            "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
            for officer in officers
            if not (
                "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,) in seen or seen.add(
                    "{0} ({1}) <{2}>".format(officer.person.common_name, officer.group.name, officer.person.email,)
                )
            )
        ]
        return result

    # def get_is_senior(self):
    #     if self.kind != self.KIND.quartet:
    #         raise ValueError('Must be quartet')
    #     Person = apps.get_model('bhs.person')
    #     midwinter = datetime.date(2020, 1, 11)
    #     persons = Person.objects.filter(
    #         members__group=self,
    #         members__status__gt=0,
    #     )
    #     if persons.count() > 4:
    #         return False
    #     all_over_55 = True
    #     total_years = 0
    #     for person in persons:
    #         try:
    #             years = int((midwinter - person.birth_date).days / 365)
    #         except TypeError:
    #             return False
    #         if years < 55:
    #             all_over_55 = False
    #         total_years += years
    #     if all_over_55 and (total_years >= 240):
    #         is_senior = True
    #     else:
    #         is_senior = False
    #     return is_senior

    # def get_roster(self):
    #     Member = apps.get_model('bhs.member')
    #     wb = Workbook()
    #     ws = wb.active
    #     fieldnames = [
    #         'BHS ID',
    #         'First Name',
    #         'Last Name',
    #         'Expiration Date',
    #         'Status',
    #     ]
    #     ws.append(fieldnames)
    #     members = self.members.filter(
    #         status=Member.STATUS.active,
    #     ).order_by('person__last_name', 'person__first_name')
    #     for member in members:
    #         bhs_id = member.person.bhs_id
    #         first_name = member.person.first_name
    #         last_name = member.person.last_name
    #         expiration = member.person.current_through
    #         status = member.person.get_status_display()
    #         row = [
    #             bhs_id,
    #             first_name,
    #             last_name,
    #             expiration,
    #             status,
    #         ]
    #         ws.append(row)
    #     file = save_virtual_workbook(wb)
    #     content = ContentFile(file)
    #     return content

    # def is_searchable(self):
    #     return bool(self.status == self.STATUS.active)

    # def owner_ids(self):
    #     return [str(owner.id) for owner in self.owners.all()]


    # Group Internals
    objects = GroupManager()

    class Meta:
        ordering = ['tree_sort']
        verbose_name_plural = 'Groups'
        constraints = [
            models.UniqueConstraint(
                name='unique_group_kind',
                fields=[
                    'bhs_id',
                    'kind',
                ]
            )
        ]

    class JSONAPIMeta:
        resource_name = "group"

    def __str__(self):
        return self.nomen

    def clean(self):
        if self.status != self.STATUS.active:
            return
        if not self.district and self.bhs_id != 1:
            raise ValidationError("Active groups must have districts.")
        if self.kind not in [
            self.KIND.chorus,
            self.KIND.quartet,
        ]:
            return
        DIVS = [
            self.DISTRICT.evg,
            self.DISTRICT.fwd,
            self.DISTRICT.lol,
            self.DISTRICT.mad,
            self.DISTRICT.ned,
            self.DISTRICT.swd,
        ]
        if self.division and self.district not in DIVS:
            raise ValidationError("Non-divisionals should not have divisions.")
        if not self.division and self.district in DIVS:
            raise ValidationError("Divisionals should have divisions.")
        if self.division:
            if self.district == self.DISTRICT.evg and not self.get_division_display().startswith('EVG'):
                    raise ValidationError("Division must be within EVG.")
            if self.district == self.DISTRICT.fwd and not self.get_division_display().startswith('FWD'):
                    raise ValidationError("Division must be within FWD.")
            if self.district == self.DISTRICT.lol and not self.get_division_display().startswith('LOL'):
                    raise ValidationError("Division must be within LOL.")
            if self.district == self.DISTRICT.mad and not self.get_division_display().startswith('MAD'):
                    raise ValidationError("Division must be within MAD.")
            if self.district == self.DISTRICT.ned and not self.get_division_display().startswith('NED'):
                    raise ValidationError("Division must be within NED.")
            if self.district == self.DISTRICT.swd and not self.get_division_display().startswith('SWD'):
                    raise ValidationError("Division must be within SWD.")
        return

        # if self.kind == self.KIND.international:
        #     if self.parent:
        #         raise ValidationError("Toplevel must be Root")
        # if self.kind in [
        #     self.KIND.district,
        #     self.KIND.noncomp,
        # ]:
        #     if self.parent.kind != self.KIND.international:
        #         raise ValidationError("Districts must have International parent.")
        # if self.kind in [
        #     self.KIND.chapter,
        # ]:
        #     if self.parent.kind not in [
        #         self.KIND.district,
        #     ]:
        #         raise ValidationError("Chapter must have District parent.")
        #     if self.division and self.parent.code not in [
        #         'EVG',
        #         'FWD',
        #         'LOL',
        #         'MAD',
        #         'NED',
        #         'SWD',
        #     ]:
        #             raise ValidationError("Non-divisionals should not have divisions.")
        #     if not self.division and self.parent.code in [
        #         'EVG',
        #         'FWD',
        #         'LOL',
        #         'MAD',
        #         'NED',
        #         'SWD',
        #     ]:
        #             raise ValidationError("Divisionals should have divisions.")
        #     if self.division:
        #         if self.parent.code == 'EVG' and not self.get_division_display().startswith('EVG'):
        #                 raise ValidationError("Division must be within EVG.")
        #         elif self.parent.code == 'FWD' and not self.get_division_display().startswith('FWD'):
        #                 raise ValidationError("Division must be within FWD.")
        #         elif self.parent.code == 'LOL' and not self.get_division_display().startswith('LOL'):
        #                 raise ValidationError("Division must be within LOL.")
        #         elif self.parent.code == 'MAD' and not self.get_division_display().startswith('MAD'):
        #                 raise ValidationError("Division must be within MAD.")
        #         elif self.parent.code == 'NED' and not self.get_division_display().startswith('NED'):
        #                 raise ValidationError("Division must be within NED.")
        #         elif self.parent.code == 'SWD' and not self.get_division_display().startswith('SWD'):
        #                 raise ValidationError("Division must be within SWD.")
        # if self.kind in [
        #     self.KIND.chorus,
        # ]:
        #     if self.parent.kind not in [
        #         self.KIND.chapter,
        #     ]:
        #         raise ValidationError("Chorus must have Chapter parent.")
        #     if self.division and self.parent.parent.code not in [
        #         'EVG',
        #         'FWD',
        #         'LOL',
        #         'MAD',
        #         'NED',
        #         'SWD',
        #     ]:
        #             raise ValidationError("Non-divisionals should not have divisions.")
        #     if self.division and self.parent.parent.code in [
        #         'EVG',
        #         'FWD',
        #         'LOL',
        #         'MAD',
        #         'NED',
        #         'SWD',
        #     ]:
        #             raise ValidationError("Divisionals should have divisions.")
        #     if self.division:
        #         if self.parent.parent.code == 'EVG' and not self.get_division_display().startswith('EVG'):
        #                 raise ValidationError("Division must be within EVG.")
        #         elif self.parent.parent.code == 'FWD' and not self.get_division_display().startswith('FWD'):
        #                 raise ValidationError("Division must be within FWD.")
        #         elif self.parent.parent.code == 'LOL' and not self.get_division_display().startswith('LOL'):
        #                 raise ValidationError("Division must be within LOL.")
        #         elif self.parent.parent.code == 'MAD' and not self.get_division_display().startswith('MAD'):
        #                 raise ValidationError("Division must be within MAD.")
        #         elif self.parent.parent.code == 'NED' and not self.get_division_display().startswith('NED'):
        #                 raise ValidationError("Division must be within NED.")
        #         elif self.parent.parent.code == 'SWD' and not self.get_division_display().startswith('SWD'):
        #                 raise ValidationError("Division must be within SWD.")
        # if self.kind in [
        #     self.KIND.quartet,
        # ] and self.parent:
        #     if self.parent.kind not in [
        #         self.KIND.district,
        #     ]:
        #         raise ValidationError("Quartet must have District parent.")
        #     if self.division and not self.parent in [
        #         'EVG',
        #         'FWD',
        #         'LOL',
        #         'MAD',
        #         'NED',
        #         'SWD',
        #     ]:
        #             raise ValidationError("Non-divisionals should not have divisions.")
        #     if not self.division and self.parent in [
        #         'EVG',
        #         'FWD',
        #         'LOL',
        #         'MAD',
        #         'NED',
        #         'SWD',
        #     ]:
        #             raise ValidationError("Divisionals should have divisions.")
        #     if self.division:
        #         if self.parent.code == 'EVG' and not self.get_division_display().startswith('EVG'):
        #                 raise ValidationError("Division must be within EVG.")
        #         elif self.parent.code == 'FWD' and not self.get_division_display().startswith('FWD'):
        #                 raise ValidationError("Division must be within FWD.")
        #         elif self.parent.code == 'LOL' and not self.get_division_display().startswith('LOL'):
        #                 raise ValidationError("Division must be within LOL.")
        #         elif self.parent.code == 'MAD' and not self.get_division_display().startswith('MAD'):
        #                 raise ValidationError("Division must be within MAD.")
        #         elif self.parent.code == 'NED' and not self.get_division_display().startswith('NED'):
        #                 raise ValidationError("Division must be within NED.")
        #         elif self.parent.code == 'SWD' and not self.get_division_display().startswith('SWD'):
        #                 raise ValidationError("Division must be within SWD.")

    # Group Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return any([
            request.user.roles.filter(name__in=[
                'SCJC',
                'Librarian',
                'Manager',
            ])
        ])

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return any([
            request.user.roles.filter(name__in=[
                'SCJC',
                'DRCJ',
                'Manager',
            ]),
            request.user in self.owners.all(),
        ])

    # Conditions:
    def can_activate(self):
        return

    # Transitions
    # @fsm_log_by
    # @fsm_log_description
    # @transition(
    #     field=status,
    #     source=[
    #         STATUS.active,
    #         STATUS.inactive,
    #         STATUS.new,
    #     ],
    #     target=STATUS.active,
    #     conditions=[
    #         can_activate,
    #     ]
    # )
    # def activate(self, description=None, *args, **kwargs):
    #     """Activate the Group."""
    #     self.denormalize()
    #     return

    # @fsm_log_by
    # @fsm_log_description
    # @transition(
    #     field=status,
    #     source=[
    #         STATUS.active,
    #         STATUS.inactive,
    #         STATUS.new,
    #     ],
    #     target=STATUS.inactive,
    # )
    # def deactivate(self, description=None, *args, **kwargs):
    #     """Deactivate the Group."""
    #     return


class Member(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
        null=True,
        blank=True,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    # Properties
    # FKs
    group = models.ForeignKey(
        'Group',
        related_name='members',
        on_delete=models.CASCADE,
    )

    person = models.ForeignKey(
        'Person',
        related_name='members',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='members',
    )

    # Internals
    objects = MemberManager()

    class Meta:
        unique_together = (
            ('group', 'person',),
        )
        verbose_name_plural = 'Members'

    class JSONAPIMeta:
        resource_name = "member"

    def __str__(self):
        return str(self.id)

    def clean(self):
        return

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        """Activate the Member."""
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Member."""
        return


class Officer(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.new,
    )

    OFFICE = Choices(
        (10, 'scjc', 'SCJC'),
        (20, 'drcj', 'DRCJ'),
        (30, 'ca', 'CA'),
        (40, 'judge', 'Judge'),
        (50, 'manager', 'Manager'),
        (60, 'librarian', 'Librarian'),
    )

    office = models.IntegerField(
        choices=OFFICE,
    )

    start_date = models.DateField(
        null=True,
        blank=True,
    )

    end_date = models.DateField(
        null=True,
        blank=True,
    )

    # FKs
    person = models.ForeignKey(
        'Person',
        related_name='officers',
        on_delete=models.CASCADE,
    )

    group = models.ForeignKey(
        'Group',
        related_name='officers',
        on_delete=models.CASCADE,
    )

    # Relations
    statelogs = GenericRelation(
        StateLog,
        related_query_name='officers',
    )

    objects = OfficerManager()

    # Properties


    # Internals
    class Meta:
        verbose_name_plural = 'Officers'

    class JSONAPIMeta:
        resource_name = "officer"

    def __str__(self):
        return str(self.id)

    def clean(self):
        pass
        # if self.group.kind != self.group.KIND.vlq:
        #     if self.office.kind != self.group.kind:
        #         raise ValidationError({
        #             'office': 'Office does not match Group Type.',
        #         })
        # else:
        #     if self.office.code != self.office.CODE.chorus_man:
        #         raise ValidationError({
        #             'office': 'VLQ officers must be Chorus Managers.',
        #         })

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        return


class Person(TimeStampedModel):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )

    STATUS = Choices(
        (-10, 'inactive', 'Inactive',),
        (0, 'new', 'New',),
        (10, 'active', 'Active',),
    )

    status = FSMIntegerField(
        help_text="""DO NOT CHANGE MANUALLY unless correcting a mistake.  Use the buttons to change state.""",
        choices=STATUS,
        default=STATUS.active,
        editable=False,
    )

    prefix = models.CharField(
        help_text="""
            The prefix of the person.""",
        max_length=255,
        blank=True,
        default='',
        editable=False,
    )

    first_name = models.CharField(
        help_text="""
            The first name of the person.""",
        max_length=255,
        editable=False,
    )

    middle_name = models.CharField(
        help_text="""
            The middle name of the person.""",
        max_length=255,
        blank=True,
        default='',
        editable=False,
    )

    last_name = models.CharField(
        help_text="""
            The last name of the person.""",
        max_length=255,
        editable=False,
    )

    nick_name = models.CharField(
        help_text="""
            The nickname of the person.""",
        max_length=255,
        blank=True,
        default='',
        editable=False,
    )

    suffix = models.CharField(
        help_text="""
            The suffix of the person.""",
        max_length=255,
        blank=True,
        default='',
        editable=False,
    )

    birth_date = models.DateField(
        blank=True,
        null=True,
        editable=False,
    )

    spouse = models.CharField(
        max_length=255,
        blank=True,
        default='',
        editable=True,
    )

    location = models.CharField(
        help_text="""
            The geographical location of the resource.""",
        max_length=255,
        blank=True,
        default='',
        editable=True,
    )

    PART = Choices(
        (1, 'tenor', 'Tenor'),
        (2, 'lead', 'Lead'),
        (3, 'baritone', 'Baritone'),
        (4, 'bass', 'Bass'),
    )

    part = models.IntegerField(
        choices=PART,
        blank=True,
        null=True,
        editable=False,
    )

    mon = models.IntegerField(
        help_text="""
            Men of Note.""",
        blank=True,
        null=True,
        editable=False,
    )

    GENDER = Choices(
        (10, '67f0002f-71bd-42b4-8e91-1f5c23802fad', 'Male'),
        (20, 'b036ccad-fc96-4dba-9c5b-95a03b6cd63a', 'Female'),
    )

    gender = models.IntegerField(
        choices=GENDER,
        blank=True,
        null=True,
        editable=False,
    )

    is_deceased = models.BooleanField(
        default=False,
        blank=True,
        editable=False,
    )
    is_honorary = models.BooleanField(
        default=False,
        blank=True,
        editable=False,
    )
    is_suspended = models.BooleanField(
        default=False,
        blank=True,
        editable=False,
    )
    is_expelled = models.BooleanField(
        default=False,
        blank=True,
        editable=False,
    )
    email = models.EmailField(
        help_text="""
            The contact email of the resource.""",
        blank=True,
        null=True,
        editable=False,
    )

    address = models.TextField(
        help_text="""
            The complete address of the resource.""",
        max_length=1000,
        blank=True,
        default='',
        editable=False,
    )

    home_phone = PhoneNumberField(
        help_text="""
            The home phone number of the resource.  Include country code.""",
        editable=False,
    )

    work_phone = PhoneNumberField(
        help_text="""
            The work phone number of the resource.  Include country code.""",
        editable=False,
    )

    cell_phone = PhoneNumberField(
        help_text="""
            The cell phone number of the resource.  Include country code.""",
        editable=False,
    )

    airports = ArrayField(
        base_field=models.CharField(
            max_length=3,
            blank=True,
            default='',
        ),
        blank=True,
        null=True,
        editable=True,
    )

    image = models.ImageField(
        upload_to=ImageUploadPath('image'),
        blank=True,
        null=True,
        editable=True,
    )

    description = models.TextField(
        help_text="""
            A bio of the person.  Max 1000 characters.""",
        max_length=1000,
        blank=True,
        default='',
        editable=True,
    )

    notes = models.TextField(
        help_text="""
            Notes (for internal use only).""",
        blank=True,
        default='',
        editable=True,
    )

    bhs_id = models.IntegerField(
        unique=True,
        editable=False,
    )

    current_through = models.DateField(
        blank=True,
        null=True,
        editable=False,
    )

    # Relations
    owners = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='persons',
        blank=True,
        editable=False
    )

    statelogs = GenericRelation(
        StateLog,
        related_query_name='persons',
    )

    # Properties
    def is_active(self):
        # For Algolia indexing
        return bool(
            self.officers.filter(
                status__gt=0,
            )
        )

    # @cached_property
    # def usernames(self):
    #     return [x.username for x in self.owners.all()]

    # @cached_property
    # def useremails(self):
    #     return [x.email for x in self.owners.all()]

    @cached_property
    def nomen(self):
        if self.nick_name:
            nick = "({0})".format(self.nick_name)
        else:
            nick = ""
        if self.bhs_id:
            suffix = "[{0}]".format(self.bhs_id)
        else:
            suffix = "[No BHS ID]"
        full = "{0} {1} {2} {3} {4}".format(
            self.first_name,
            self.middle_name,
            self.last_name,
            nick,
            suffix,
        )
        return " ".join(full.split())

    @cached_property
    def name(self):
        return self.common_name

    @cached_property
    def full_name(self):
        if self.nick_name:
            nick = "({0})".format(self.nick_name)
        else:
            nick = ""
        full = "{0} {1} {2} {3}".format(
            self.first_name,
            self.middle_name,
            self.last_name,
            nick,
        )
        return " ".join(full.split())

    @cached_property
    def common_name(self):
        if self.nick_name:
            first = self.nick_name
        else:
            first = self.first_name
        return "{0} {1}".format(first, self.last_name)

    @cached_property
    def sort_name(self):
        return "{0}, {1}".format(self.last_name, self.first_name)

    @cached_property
    def initials(self):
        one = self.nick_name or self.first_name
        two = str(self.last_name)
        if not (one and two):
            return "--"
        return "{0}{1}".format(
            one[0].upper(),
            two[0].upper(),
        )

    @cached_property
    def image_id(self):
        return self.image.name or 'missing_image'

    def image_url(self):
        try:
            return self.image.url
        except ValueError:
            return 'https://res.cloudinary.com/barberscore/image/upload/v1554830585/missing_image.jpg'

    # @cached_property
    # def current_through(self):
    #     try:
    #         current_through = self.members.get(
    #             group__bhs_id=1,
    #         ).end_date
    #     except self.members.model.DoesNotExist:
    #         current_through = None
    #     return current_through

    # @cached_property
    # def current_status(self):
    #     today = now().date()
    #     if self.current_through:
    #         if self.current_through >= today:
    #             return True
    #         return False
    #     return True

    # @cached_property
    # def current_district(self):
    #     return bool(
    #         self.members.filter(
    #             group__kind=11, # hardcoded for convenience
    #             status__gt=0,
    #         )
    #     )

    # Internals
    objects = PersonManager()

    class Meta:
        verbose_name_plural = 'Persons'

    class JSONAPIMeta:
        resource_name = "person"

    def clean(self):
        pass

    def __str__(self):
        return self.nomen

    # Person Methods
    def update_owners(self):
        User = get_user_model()
        owners = User.objects.filter(
            email=self.email,
        )
        return self.owners.set(owners)

    # Permissions
    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_read_permission(request):
        return True

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_read_permission(self, request):
        return True

    @staticmethod
    @allow_staff_or_superuser
    @authenticated_users
    def has_write_permission(request):
        return False

    @allow_staff_or_superuser
    @authenticated_users
    def has_object_write_permission(self, request):
        return False

    # Transitions
    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.active)
    def activate(self, description=None, *args, **kwargs):
        """Activate the Person."""
        return

    @fsm_log_by
    @fsm_log_description
    @transition(field=status, source='*', target=STATUS.inactive)
    def deactivate(self, description=None, *args, **kwargs):
        """Deactivate the Person."""
        return
