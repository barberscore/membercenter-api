

# Standard Library
import datetime
import logging

# Django
from django.apps import apps
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


log = logging.getLogger('updater')

from apps.bhs.tasks import create_or_update_member_from_join


class Command(BaseCommand):
    help = "Nightly rebuild."

    def handle(self, *args, **options):
        # Group = apps.get_model('bhs.group')
        # Group.objects.sort_tree()
        # Award = apps.get_model('bhs.award')
        # Award.objects.sort_tree()

        Join = apps.get_model('source.join')
        # Sync Members
        self.stdout.write("Fetching Joins from Source Database...")
        joins = Join.objects.export_values(cursor=None)
        t = len(joins)
        i = 0
        for join in joins:
            i += 1
            self.stdout.flush()
            self.stdout.write("Updating {0} of {1} Members...".format(i, t), ending='\r')
            create_or_update_member_from_join.delay(join)
        self.stdout.write("")
        self.stdout.write("Updated {0} Members.".format(t))
        # Delete Orphans
        # self.stdout.write("Deleting orphans...")
        # joins = list(Join.objects.values_list('id', flat=True))
        # t = Member.objects.delete_orphans(joins)
        # self.stdout.write("Deleted {0} Member orphans.".format(t)
        self.stdout.write("Complete.")
        return
