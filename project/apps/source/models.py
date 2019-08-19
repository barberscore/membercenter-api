# Django
from django.db import models

# Local
from .managers import HumanManager
from .managers import JoinManager
from .managers import RoleManager
from .managers import StructureManager


class Human(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        editable=False,
    )
    username = models.CharField(
        max_length=60,
        editable=False,
    )
    first_name = models.CharField(
        max_length=45,
        editable=False,
    )
    middle_name = models.CharField(
        max_length=45,
        editable=False,
        db_column='middle_initial',
    )
    last_name = models.CharField(
        max_length=45,
        editable=False,
    )
    nick_name = models.CharField(
        max_length=45,
        editable=False,
        db_column='preferred_name',
    )
    email = models.CharField(
        max_length=255,
        editable=False,
    )
    birth_date = models.DateField(
        editable=False,
        db_column='birthday'
    )
    is_deceased = models.BooleanField(
        editable=False,
    )
    created = models.DateTimeField(
        db_column='created',
        editable=False,
    )
    created_by_id = models.CharField(
        max_length=36,
        null=True,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        editable=False,
    )
    modified_by_id = models.CharField(
        max_length=36,
        null=True,
        editable=False,
        db_column='updated_by_id',
    )
    deleted = models.DateTimeField(
        db_column='deleted',
        editable=False,
    )
    deleted_by_id = models.CharField(
        max_length=36,
        null=True,
        editable=False,
    )
    home_phone = models.CharField(
        max_length=20,
        editable=False,
        db_column='phone'
    )
    cell_phone = models.CharField(
        max_length=20,
        editable=False,
    )
    work_phone = models.CharField(
        max_length=20,
        editable=False,
    )
    bhs_id = models.IntegerField(
        editable=False,
        unique=True,
        db_column='legacy_id',
    )
    gender = models.CharField(
        max_length=15,
        editable=False,
        db_column='sex',
    )
    part = models.CharField(
        max_length=10,
        editable=False,
        db_column='primary_voice_part',
    )
    is_honorary = models.BooleanField(
        editable=False,
        db_column='honorary_member',
    )
    is_suspended = models.BooleanField(
        editable=False,
    )
    merged_id = models.CharField(
        max_length=36,
        null=True,
        editable=False,
        db_column='merged_into',
    )
    mon = models.IntegerField(
        editable=False,
        db_column='trusted_mon',
    )
    is_expelled = models.BooleanField(
        editable=False,
    )
    objects = HumanManager()

    # Internals
    def __str__(self):
        if self.nick_name:
            first = self.nick_name
        else:
            first = self.first_name
        return " ".join([
            first,
            self.last_name,
        ])

    # Methods
    class Meta:
        managed = False
        db_table = 'vwMembers'


class Structure(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        editable=False,
    )
    kind = models.CharField(
        max_length=15,
        editable=False,
        db_column='object_type',
    )
    gender = models.CharField(
        max_length=100,
        editable=False,
        db_column='category'
    )
    county = models.CharField(
        max_length=45,
        editable=False,
    )
    country = models.CharField(
        max_length=45,
        editable=False,
    )
    bhs_id = models.IntegerField(
        editable=False,
        unique=True,
        null=True,
        db_column='legacy_id',
    )
    chapter_code = models.CharField(
        max_length=45,
        editable=False,
        db_column='legacy_code',
    )
    chorus_name = models.CharField(
        max_length=45,
        editable=False,
    )
    website = models.CharField(
        max_length=255,
        editable=False,
    )
    tin = models.CharField(
        max_length=18,
        editable=False,
        db_column='TIN',
    )
    established_date = models.DateField(
        editable=False,
    )
    visitor_information = models.TextField(
        editable=False,
    )
    created = models.DateTimeField(
        db_column='created',
        editable=False,
    )
    created_by_id = models.CharField(
        max_length=36,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        editable=False,
    )
    modified_by_id = models.CharField(
        max_length=36,
        editable=False,
        db_column='updated_by_id',
    )
    deleted = models.DateTimeField(
        db_column='deleted',
        editable=False,
    )
    deleted_by_id = models.CharField(
        max_length=36,
        editable=False,
    )
    phone = models.CharField(
        max_length=16,
        editable=False,
    )
    phone_ext = models.CharField(
        max_length=16,
        editable=False,
    )
    fax = models.CharField(
        max_length=16,
        editable=False,
    )
    email = models.CharField(
        max_length=255,
        editable=False,
    )
    facebook = models.CharField(
        max_length=255,
        editable=False,
    )
    twitter = models.CharField(
        max_length=255,
        editable=False,
    )
    youtube = models.CharField(
        max_length=255,
        editable=False,
    )
    pinterest = models.CharField(
        max_length=255,
        editable=False,
    )
    flickr = models.CharField(
        max_length=255,
        editable=False,
    )
    instagram = models.CharField(
        max_length=255,
        editable=False,
    )
    soundcloud = models.CharField(
        max_length=255,
        editable=False,
    )
    preferred_name = models.CharField(
        max_length=128,
        editable=False,
    )
    first_alternate_name = models.CharField(
        max_length=128,
        editable=False,
    )
    second_alternate_name = models.CharField(
        max_length=128,
        editable=False,
    )
    is_default = models.BooleanField(
        editable=False,
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='children',
        db_column='parent_id',
        on_delete=models.SET_NULL,
    )
    division = models.CharField(
        max_length=255,
        editable=False,
    )
    status = models.ForeignKey(
        'Status',
        related_name='structures',
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )
    licenced_date = models.DateField(
        editable=False,
    )
    chartered_date = models.DateField(
        editable=False,
    )
    lft = models.IntegerField(
        editable=False,
    )
    rght = models.IntegerField(
        editable=False,
    )

    # FKs
    objects = StructureManager()

    def __str__(self):
        if self.name:
            name = self.name.strip()
        else:
            name = 'UNKNOWN'
        return "{0} [{1}]".format(
            name,
            self.bhs_id,
        )


    class Meta:
        managed = False
        db_table = 'vwStructures'


class Status(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    name = models.CharField(
        max_length=36,
        editable=False,
    )
    label = models.CharField(
        max_length=36,
        editable=False,
    )
    non_admin_view = models.BooleanField(
        editable=False,
    )
    non_admin_join = models.BooleanField(
        editable=False,
    )
    renewable = models.BooleanField(
        editable=False,
    )
    entities = models.TextField(
        editable=False,
    )

    # Internals
    def __str__(self):
        return str(self.name)

    class Meta:
        managed = False
        db_table = 'vwStatuses'
        verbose_name_plural = 'statuses'


class Membership(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    object_type = models.CharField(
        max_length=36,
        editable=False,
    )
    structure = models.ForeignKey(
        'Structure',
        related_name='memberships',
        null=True,
        editable=False,
        db_column='object_id',
        on_delete=models.SET_NULL,
    )
    months = models.IntegerField(
        editable=False,
    )
    is_auto_renew = models.BooleanField(
        default=False,
        db_column='auto_renew',
    )
    type = models.CharField(
        max_length=36,
        editable=False,
    )
    code = models.CharField(
        max_length=4,
        editable=False,
    )
    membership_options_id = models.CharField(
        max_length=36,
        editable=False,
    )
    effective_date = models.DateField(
        editable=False,
    )
    created = models.DateTimeField(
        db_column='created',
        editable=False,
    )
    created_by_id = models.CharField(
        max_length=36,
        editable=False,
    )
    deleted = models.DateTimeField(
        db_column='deleted',
        editable=False,
    )
    deleted_by_id = models.CharField(
        max_length=36,
        editable=False,
    )
    modified = models.DateTimeField(
        editable=False,
    )
    status = models.ForeignKey(
        'Status',
        related_name='memberships',
        null=True,
        editable=False,
        on_delete=models.SET_NULL,
    )

    # Internals
    def __str__(self):
        return "{0} {1}".format(
            self.structure,
            self.code,
        )

    class Meta:
        managed = False
        db_table = 'vwMemberships'


class Subscription(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    members_entities_id = models.CharField(
        max_length=36,
        editable=False,
    )
    modified = models.DateTimeField(
        null=True,
        editable=False,
        db_column='updated',
    )
    current_through = models.DateField(
        db_column='valid_through',
        null=True,
        editable=False,
    )
    memberships_id = models.CharField(
        max_length=36,
        editable=False,
    )
    created = models.DateTimeField(
        null=True,
        editable=False,
    )
    status = models.CharField(
        max_length=36,
        editable=False,
    )
    human = models.ForeignKey(
        'Human',
        related_name='subscriptions',
        editable=False,
        db_column='members_id',
        on_delete=models.CASCADE,
    )
    join_date = models.DateField(
        null=True,
        editable=False,
    )
    items_editable = models.BooleanField(
        editable=False,
    )
    deleted = models.DateTimeField(
        null=True,
        editable=False,
        db_column='deleted',
    )

    # Internals
    def __str__(self):
        return str(self.human)

    class Meta:
        managed = False
        db_table = 'vwSubscriptions'


class Role(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    object_type = models.CharField(
        max_length=32,
        editable=False,
    )
    structure = models.ForeignKey(
        'Structure',
        related_name='roles',
        editable=False,
        db_column='object_id',
        on_delete=models.CASCADE,
    )
    officer_roles_id = models.CharField(
        max_length=36,
        editable=False,
    )
    name = models.CharField(
        max_length=100,
        editable=False,
    )
    abbv = models.CharField(
        max_length=10,
        editable=False,
    )
    start_date = models.DateField(
        null=True,
        editable=False,
    )
    end_date = models.DateField(
        null=True,
        editable=False,
    )
    # FKs
    human = models.ForeignKey(
        'Human',
        related_name='roles',
        null=True,
        editable=False,
        db_column='member_id',
        on_delete=models.SET_NULL,
    )

    created = models.DateTimeField(
        db_column='created',
        null=True,
        editable=False,
    )
    modified = models.DateTimeField(
        db_column='updated',
        null=True,
        editable=False,
    )

    objects = RoleManager()

    # Internals
    def __str__(self):
        return "{0} {1} {2}".format(
            self.name,
            self.human,
            self.structure,
        )

    class Meta:
        managed = False
        db_table = 'vwOfficers'


class Join(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=255,
        editable=False,
    )
    subscription = models.ForeignKey(
        'Subscription',
        editable=False,
        related_name='joins',
        on_delete=models.CASCADE,
    )
    membership = models.ForeignKey(
        'Membership',
        editable=False,
        related_name='joins',
        on_delete=models.CASCADE,
    )
    status = models.BooleanField(
        editable=False,
    )
    established_date = models.DateField(
        db_column='created',
        null=True,
        editable=False,
    )
    inactive_date = models.DateField(
        db_column='inactive',
        null=True,
        editable=False,
    )
    inactive_reason = models.CharField(
        max_length=50,
        db_column='inactive_reason',
        editable=False,
    )
    paid = models.BooleanField(
        editable=False,
    )
    part = models.CharField(
        max_length=10,
        editable=False,
        db_column='vocal_part',
    )
    structure = models.ForeignKey(
        'Structure',
        editable=False,
        related_name='joins',
        db_column='reference_structure_id',
        on_delete=models.CASCADE,
    )
    modified = models.DateTimeField(
        db_column='modified',
        null=True,
        editable=False,
    )
    created = models.DateTimeField(
        db_column='created_on',
        null=True,
        editable=False,
    )
    deleted = models.DateTimeField(
        null=True,
        editable=False,
        db_column='deleted',
    )
    objects = JoinManager()

    # FKs

    # Internals
    def __str__(self):
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'vwSubscriptions_Memberships'
        verbose_name = 'Join'
        verbose_name_plural = 'Joins'


class Address(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=36,
        editable=False,
    )
    name = models.CharField(
        max_length=75,
        editable=False,
    )
    object_type = models.CharField(
        max_length=36,
        editable=False,
    )
    object_id = models.CharField(
        max_length=36,
        editable=False,
    )
    kind = models.CharField(
        max_length=36,
        editable=False,
        db_column='type',
    )
    city = models.CharField(
        max_length=128,
        editable=False,
    )
    state = models.CharField(
        max_length=64,
        editable=False,
    )
    country = models.CharField(
        max_length=32,
        editable=False,
    )
    status = models.BooleanField(
        editable=False,
    )
    updated = models.DateTimeField(
        null=True,
        editable=False,
    )
    modified = models.DateTimeField(
        null=True,
        editable=False,
    )
    created = models.DateTimeField(
        null=True,
        editable=False,
    )
    lat = models.FloatField(
        null=True,
        editable=False,
    )
    lon = models.FloatField(
        null=True,
        editable=False,
    )
    legacy_id = models.IntegerField(
        editable=False,
    )
    deleted = models.DateTimeField(
        null=True,
        editable=False,
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        managed = False
        db_table = 'vwAddresses'
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'
