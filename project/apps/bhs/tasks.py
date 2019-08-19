import django
django.setup()

# Third-Party
from django_rq import job

# Django
from django.apps import apps


@job('low')
def create_or_update_group_from_structure(structure):
    Group = apps.get_model('bhs.group')
    return Group.objects.update_or_create_from_structure(structure)


@job('low')
def create_or_update_person_from_human(human):
    Person = apps.get_model('bhs.person')
    return Person.objects.update_or_create_from_human(human)


@job('low')
def create_or_update_officer_from_role(role):
    Officer = apps.get_model('bhs.officer')
    return Officer.objects.update_or_create_from_role(role)


@job('low')
def create_or_update_member_from_join(join):
    Member = apps.get_model('bhs.member')
    return Member.objects.update_or_create_from_join(join)
