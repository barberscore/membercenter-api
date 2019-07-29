


# Standard Library
import datetime
import rest_framework_jwt
# Third-Party
from factory import Faker  # post_generation,
from factory import Iterator
from factory import LazyAttribute
from factory import PostGenerationMethodCall
from factory import RelatedFactory
from factory import Sequence
from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.django import mute_signals
from factory.fuzzy import FuzzyInteger

# Django
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save

# First-Party

from rest_framework_jwt.models import User

from apps.bhs.models import Group
from apps.bhs.models import Member
from apps.bhs.models import Officer
from apps.bhs.models import Person



class GroupFactory(DjangoModelFactory):
    name = Faker('company')
    status = Group.STATUS.active
    kind = Group.KIND.quartet
    code = ''
    start_date = None
    end_date = None
    email = Faker('email')
    phone = Faker('phone_number')
    location = ''
    website = ''
    facebook = ''
    twitter = ''
    image = ''
    description = ''
    notes = ''
    bhs_id = Sequence(lambda x: x)
    parent = None

    class Meta:
        model = Group

    # @post_generation
    # def create_members(self, create, extracted, **kwargs):
    #     if create:
    #         if self.kind == self.KIND.quartet:
    #             size = 4
    #         else:
    #             size = 20
    #         for i in range(size):
    #             MemberFactory.create(group=self)

    # @post_generation
    # def create_repertories(self, create, extracted, **kwargs):
    #     if create:
    #         for i in range(6):
    #             RepertoryFactory.create(group=self)


class MemberFactory(DjangoModelFactory):
    status = Member.STATUS.active
    part = Iterator([
        Member.PART.tenor,
        Member.PART.lead,
        Member.PART.baritone,
        Member.PART.bass,
    ])
    group = SubFactory('factories.GroupFactory')
    person = SubFactory('factories.PersonFactory')

    class Meta:
        model = Member


class OfficerFactory(DjangoModelFactory):
    status = Officer.STATUS.new
    start_date = None
    end_date = None
    office = 410
    person = SubFactory('factories.PersonFactory')
    group = SubFactory('factories.GroupFactory')

    class Meta:
        model = Officer



@mute_signals(pre_delete, post_save)
class PersonFactory(DjangoModelFactory):
    # name = Faker('name_male')
    first_name = Faker('first_name_male')
    middle_name = ''
    last_name = Faker('last_name_male')
    nick_name = ''
    status = Person.STATUS.active
    birth_date = None
    location = ''
    website = ''
    email = None
    image = ''
    description = ''
    notes = ''
    bhs_id = Sequence(lambda x: '1{0:05d}'.format(x))

    class Meta:
        model = Person



@mute_signals(pre_delete, post_save)
class UserFactory(DjangoModelFactory):
    username = Faker('uuid4')
    password = PostGenerationMethodCall('set_password', 'password')
    is_staff = False

    class Meta:
        model = User
