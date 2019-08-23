from datetime import date

# Third-Party
from factory import Faker  # post_generation,
from factory import PostGenerationMethodCall
# from factory import RelatedFactory
from factory import Sequence
# from factory import SubFactory
from factory.django import DjangoModelFactory
from factory.django import mute_signals
# from factory.fuzzy import FuzzyInteger
from factory.fuzzy import FuzzyDate
# Django
from django.db.models.signals import m2m_changed
from django.db.models.signals import pre_delete
from django.db.models.signals import pre_save

# First-Party
from rest_framework_jwt.models import User
from apps.bhs.models import Group
from apps.bhs.models import Person


class GroupFactory(DjangoModelFactory):
    name = Faker('company')
    status = Group.STATUS.active
    kind = Group.KIND.quartet
    gender = Group.KIND.quartet
    district = Group.DISTRICT.bhs
    bhs_id = Sequence(lambda x: '1{0:05d}'.format(x))

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


class PersonFactory(DjangoModelFactory):
    status = Person.STATUS.active
    first_name = Faker('first_name_male')
    last_name = Faker('last_name_male')
    part = Person.PART.lead
    gender = Person.GENDER.male
    bhs_id = Sequence(lambda x: '1{0:05d}'.format(x))
    current_through = FuzzyDate(date(2030, 1, 1), date(2030, 1, 1))

    class Meta:
        model = Person


@mute_signals(pre_delete, pre_save, m2m_changed)
class UserFactory(DjangoModelFactory):
    id = Faker('uuid4')
    name = Faker('name_male')
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', 'password')
    is_staff = False

    class Meta:
        model = User
