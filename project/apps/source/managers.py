
# Standard Library
from datetime import date

# Django
from django.contrib.auth import get_user_model
from django.db.models import Case
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import F
from django.db.models import IntegerField
from django.db.models import Manager
from django.db.models import Max
from django.db.models import Min
from django.db.models import OuterRef
from django.db.models import Q
from django.db.models import Subquery
from django.db.models import When


User = get_user_model()

class HumanManager(Manager):
    def export_values(self, cursor=None):
        today = date.today()
        hs = self.filter(
            Q(merged_id="") | Q(merged_id=None),
            Q(deleted_by_id="") | Q(deleted_by_id=None),
        )
        if cursor:
            hs = hs.filter(
                Q(modified__gte=cursor) | Q(subscriptions__modified__gte=cursor),
            )
        hs = hs.annotate(
            current_through=Max(
                'subscriptions__current_through',
                filter=Q(
                    subscriptions__items_editable=True,
                    subscriptions__deleted__isnull=True,
                    subscriptions__current_through__gt='0001-01-01',
                ),
            ),
            status=Case(
                When(current_through__gte=today, then=10),
                default=-10,
                output_field=IntegerField(),
            ),
        )

        return list(hs.values(
            'id',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'email',
            'birth_date',
            'home_phone',
            'cell_phone',
            'work_phone',
            'bhs_id',
            'gender',
            'part',
            'mon',
            'is_deceased',
            'is_honorary',
            'is_suspended',
            'is_expelled',
            'status',
            'current_through',
        ))


class StructureManager(Manager):
    def export_values(self, cursor=None):
        output = []
        types = [
            'organization',
            'district',
            'group',
            'chapter',
            'chorus',
            'quartet',
        ]
        for t in types:
            ss = self.filter(
                Q(kind=t),
                Q(deleted_by_id="") | Q(deleted_by_id=None),
            )
            if cursor:
                ss = ss.filter(
                    modified__gte=cursor,
                )
            output.extend(
                list(ss.values(
                    'id',
                    'name',
                    'kind',
                    'gender',
                    'division',
                    'bhs_id',
                    'chapter_code',
                    'website',
                    'email',
                    'phone',
                    'fax',
                    'facebook',
                    'twitter',
                    'youtube',
                    'pinterest',
                    'flickr',
                    'instagram',
                    'soundcloud',
                    'preferred_name',
                    'visitor_information',
                    'established_date',
                    'status_id',
                    'parent_id',
                ))
            )
        return output


class RoleManager(Manager):
    def export_values(self, cursor=None):
        today = date.today()
        rs = self.filter(
            Q(structure__deleted_by_id="") | Q(structure__deleted_by_id=None),
            Q(human__merged_id="") | Q(human__merged_id=None),
            Q(human__deleted_by_id="") | Q(human__deleted_by_id=None),
        )
        if cursor:
            rs = rs.filter(
                modified__gte=cursor,
            )
        return list(rs.values(
            'name',
            'human_id',
            'structure_id',
        ).annotate(
            id=Max('id'),
            startest_date=Min('start_date'),
            endest_date=Max('end_date'),
            status=Case(
                When(endest_date=None, then=10),
                When(endest_date__gte=today, then=10),
                default=-10,
                output_field=IntegerField(),
            ),
        ))


class JoinManager(Manager):
    def export_values(self, cursor=None):
        today = date.today()
        js = self.select_related(
            'structure',
            'membership',
            'subscription',
            'subscription__human',
        ).filter(
            Q(paid=True),
            Q(deleted__isnull=True),
            Q(membership__deleted_by_id="") | Q(membership__deleted_by_id=None),
            Q(subscription__deleted=None),
            Q(structure__deleted_by_id="") | Q(structure__deleted_by_id=None),
            Q(subscription__human__merged_id="") | Q(subscription__human__merged_id=None),
            Q(subscription__human__deleted_by_id="") | Q(subscription__human__deleted_by_id=None),
        )
        if cursor:
            js = js.filter(
                Q(modified__gte=cursor) |
                Q(membership__modified__gte=cursor) |
                Q(subscription__modified__gte=cursor)
            )
        js = js.values(
            'structure__id',
            'subscription__human__id',
        )
        js = js.annotate(
            id=Max('id'),
            vocal_part=Subquery(
                self.filter(
                    structure__id=OuterRef('structure__id'),
                    subscription__human__id=OuterRef('subscription__human__id'),
                ).order_by(
                    '-modified',
                ).values('part')[:1],
                output_field=CharField()
            ),
            inactivist_date=Subquery(
                self.filter(
                    structure__id=OuterRef('structure__id'),
                    subscription__human__id=OuterRef('subscription__human__id'),
                ).order_by(
                    F('inactive_date').desc(nulls_first=True)
                ).values('inactive_date')[:1],
                output_field=DateField()
            ),
            currentest_date=Subquery(
                self.filter(
                    structure__id=OuterRef('structure__id'),
                    subscription__human__id=OuterRef('subscription__human__id'),
                ).order_by(
                    F('subscription__current_through').desc(nulls_first=True)
                ).values('subscription__current_through')[:1],
                output_field=DateField()
            ),
            startest_date=Min('established_date'),
            endest_date=Case(
                When(
                    Q(
                        structure__kind__in=[
                            'chorus',
                            'chapter',
                        ],
                    ),
                    then=F('inactivist_date'),
                ),
                default=F('currentest_date'),
                output_field=DateField(),
            ),
            status=Case(
                When(endest_date__isnull=True, then=10),
                When(endest_date__gte=today, then=10),
                default=-10,
                output_field=IntegerField(),
            ),
        ).values(
            'structure__id',
            'subscription__human__id',
            'id',
            'vocal_part',
            'startest_date',
            'endest_date',
            'status',
        )
        return list(js)
