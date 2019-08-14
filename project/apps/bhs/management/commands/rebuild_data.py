

# Standard Library
import datetime
import logging

# Django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


log = logging.getLogger('updater')


class Command(BaseCommand):
    help = "Nightly rebuild."

    def handle(self, *args, **options):
        # Group = apps.get_model('bhs.group')
        # Group.objects.sort_tree()
        # Award = apps.get_model('bhs.award')
        # Award.objects.sort_tree()

        Join = apps.get_model('source.join')
        Member = apps.get_model('bhs.member')
        User = get_user_model()
        # Sync Members
        self.stdout.write("Fetching Joins from Source Database...")
        joins = Join.objects.export_values(cursor=None)
        t = len(joins)
        i = 0
        for join in joins:
            i += 1
            self.stdout.flush()
            self.stdout.write("Updating {0} of {1} Members...".format(i, t), ending='\r')
            try:
                member, _ = Member.objects.update_or_create_from_join(join)
            except Exception as e:
                log.error(e)
                continue
            # Update User if account?
            if member.group.bhs_id == 1:
                person = member.person
                person.current_through = member.end_date
                person.status = member.status
                person.save()
                user, _ = User.objects.get_or_create(
                    email=person.email,
                    name=person.name,
                    first_name=person.first_name,
                    last_name=person.last_name,
                )
                person.owners.add(user)
        self.stdout.write("")
        self.stdout.write("Updated {0} Members.".format(t))
        # if not cursor:
        #     self.stdout.write("Deleting orphans...")
        #     joins = list(Join.objects.values_list('id', flat=True))
        #     t = Member.objects.delete_orphans(joins)
        #     self.stdout.write("Deleted {0} Member orphans.".format(t)
        return
