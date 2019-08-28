# Third-Party
# from algoliasearch_django.decorators import disable_auto_indexing
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from phonenumber_field.validators import validate_international_phonenumber

# Django
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.db.models import Manager
# from django.core.validators import validate_email
from .validators import validate_url
from .validators import validate_phone
from .validators import validate_email

User = get_user_model()


class GroupManager(Manager):
    def update_or_create_from_structure(self, structure):
        # Extract
        if not isinstance(structure, dict):
            raise ValueError("Must be dict")
        mc_pk = structure['id']
        name = structure['name']
        status = structure['status_real']
        kind = structure['kind']
        gender = structure['gender']
        district = structure['district']
        division = structure['division']
        bhs_id = structure['bhs_id']
        legacy_code = structure['chapter_code']
        website = structure['website']
        email = structure['email']
        main_phone = structure['phone']
        fax_phone = structure['fax']
        facebook = structure['facebook']
        twitter = structure['twitter']
        youtube = structure['youtube']
        pinterest = structure['pinterest']
        flickr = structure['flickr']
        instagram = structure['instagram']
        soundcloud = structure['soundcloud']
        preferred_name = structure['preferred_name']
        visitor_information = structure['visitor_information']
        established_date = structure['established_date']

        # Re-construct dangling article
        name = name.strip() if name else ""
        parsed = name.partition(", The")
        name = "The {0}".format(parsed[0]) if parsed[1] else parsed[0]

        preferred_name = "{0} (NAME APPROVAL PENDING)".format(preferred_name.strip()) if preferred_name else ''
        name = name if name else preferred_name

        if not name:
            name = "(UNKNOWN)"

        # AIC
        aic_map = {
            503061: "Signature",
            500983: "After Hours",
            501972: "Main Street",
            501329: "Forefront",
            500922: "Instant Classic",
            304772: "Musical Island Boys",
            500000: "Masterpiece",
            501150: "Ringmasters",
            317293: "Old School",
            286100: "Storm Front",
            500035: "Crossroads",
            297201: "OC Times",
            299233: "Max Q",
            302244: "Vocal Spectrum",
            299608: "Realtime",
            6158: "Gotcha!",
            2496: "Power Play",
            276016: "Four Voices",
            5619: "Michigan Jake",
            6738: "Platinum",
            3525: "FRED",
            5721: "Revival",
            2079: "Yesteryear",
            2163: "Nightlife",
            4745: "Marquis",
            3040: "Joker's Wild",
            1259: "Gas House Gang",
            2850: "Keepsake",
            1623: "The Ritz",
            3165: "Acoustix",
            1686: "Second Edition",
            492: "Chiefs of Staff",
            1596: "Interstate Rivals",
            1654: "Rural Route 4",
            406: "The New Tradition",
            1411: "Rapscallions",
            1727: "Side Street Ramblers",
            545: "Classic Collection",
            490: "Chicago News",
            329: "Boston Common",
            4034: "Grandma's Boys",
            318: "Bluegrass Student Union",
            362: "Most Happy Fellows",
            1590: "Innsiders",
            1440: "Happiness Emporium",
            1427: "Regents",
            627: "Dealer's Choice",
            1288: "Golden Staters",
            1275: "Gentlemen's Agreement",
            709: "Oriole Four",
            711: "Mark IV",
            2047: "Western Continentals",
            1110: "Four Statesmen",
            713: "Auto Towners",
            715: "Four Renegades",
            1729: "Sidewinders",
            718: "Town and Country 4",
            719: "Gala Lads",
            1871: "The Suntones",
            722: "Evans Quartet",
            724: "Four Pitchikers",
            726: "Gaynotes",
            729: "Lads of Enchantment",
            731: "Confederates",
            732: "Four Hearsemen",
            736: "The Orphans",
            739: "Vikings",
            743: "Four Teens",
            746: "Schmitt Brothers",
            748: "Buffalo Bills",
            750: "Mid-States Four",
            753: "Pittsburghers",
            756: "Doctors of Harmony",
            759: "Garden State Quartet",
            761: "Misfits",
            764: "Harmony Halls",
            766: "Four Harmonizers",
            770: "Elastic Four",
            773: "Chord Busters",
            775: "Flat Foot Four",
            776: "Bartlsesville Barflies",
        }

        # Overwrite status for AIC
        if bhs_id in aic_map:
            status = -5

        # Overwrite name for AIC
        name = aic_map.get(bhs_id, name)

        kind_map = {
            'quartet': self.model.KIND.quartet,
            'chorus': self.model.KIND.chorus,
            'chapter': self.model.KIND.chapter,
            'group': self.model.KIND.noncomp,
            'district': self.model.KIND.district,
            'organization': self.model.KIND.international,
        }
        kind = kind_map.get(kind, None)

        legacy_code = legacy_code if legacy_code else ""

        gender_map = {
            'men': self.model.GENDER.male,
            'women': self.model.GENDER.female,
            'mixed': self.model.GENDER.mixed,
        }
        gender = gender_map.get(gender, self.model.GENDER.male)

        district_map = {
            'BHS': self.model.DISTRICT.bhs,
            'CAR': self.model.DISTRICT.car,
            'CSD': self.model.DISTRICT.csd,
            'DIX': self.model.DISTRICT.dix,
            'EVG': self.model.DISTRICT.evg,
            'FWD': self.model.DISTRICT.fwd,
            'ILL': self.model.DISTRICT.ill,
            'JAD': self.model.DISTRICT.jad,
            'LOL': self.model.DISTRICT.lol,
            'MAD': self.model.DISTRICT.mad,
            'NED': self.model.DISTRICT.ned,
            'NSC': self.model.DISTRICT.nsc,
            'ONT': self.model.DISTRICT.ont,
            'PIO': self.model.DISTRICT.pio,
            'RMD': self.model.DISTRICT.rmd,
            'SLD': self.model.DISTRICT.sld,
            'SUN': self.model.DISTRICT.sun,
            'SWD': self.model.DISTRICT.swd,
        }
        district = district_map.get(district, None)

        division_map = {
            'EVG Division I': self.model.DIVISION.evgd1,
            'EVG Division II': self.model.DIVISION.evgd2,
            'EVG Division III': self.model.DIVISION.evgd3,
            'EVG Division IV': self.model.DIVISION.evgd4,
            'EVG Division V': self.model.DIVISION.evgd5,
            'FWD Arizona': self.model.DIVISION.fwdaz,
            'FWD Northeast': self.model.DIVISION.fwdne,
            'FWD Northwest': self.model.DIVISION.fwdnw,
            'FWD Southeast': self.model.DIVISION.fwdse,
            'FWD Southwest': self.model.DIVISION.fwdsw,
            'LOL 10000 Lakes': self.model.DIVISION.lol10l,
            'LOL Division One': self.model.DIVISION.lolone,
            'LOL Northern Plains': self.model.DIVISION.lolnp,
            'LOL Packerland': self.model.DIVISION.lolpkr,
            'LOL Southwest': self.model.DIVISION.lolsw,
            'MAD Central': self.model.DIVISION.madcen,
            'MAD Northern': self.model.DIVISION.madnth,
            'MAD Southern': self.model.DIVISION.madsth,
            'NED Granite and Pine': self.model.DIVISION.nedgp,
            'NED Mountain': self.model.DIVISION.nedmtn,
            'NED Patriot': self.model.DIVISION.nedpat,
            'NED Sunrise': self.model.DIVISION.nedsun,
            'NED Yankee': self.model.DIVISION.nedyke,
            'SWD Northeast': self.model.DIVISION.swdne,
            'SWD Northwest': self.model.DIVISION.swdnw,
            'SWD Southeast': self.model.DIVISION.swdse,
            'SWD Southwest': self.model.DIVISION.swdsw,
        }
        division = division_map.get(division, None)

        website = validate_url(website)
        facebook = validate_url(facebook)
        twitter = validate_url(twitter)
        youtube = validate_url(youtube)
        pinterest = validate_url(pinterest)
        flickr = validate_url(flickr)
        instagram = validate_url(instagram)
        soundcloud = validate_url(soundcloud)

        phone = validate_phone(main_phone)
        fax_phone = validate_phone(fax_phone)

        email = validate_email(email)

        visitor_information = visitor_information.strip() if visitor_information else ''

        defaults = {
            'status': status,
            'name': name,
            'kind': kind,
            'gender': gender,
            'district': district,
            'division': division,
            'bhs_id': bhs_id,
            'code': legacy_code,
            'website': website,
            'email': email,
            'phone': phone,
            'fax_phone': fax_phone,
            'facebook': facebook,
            'twitter': twitter,
            'youtube': youtube,
            'pinterest': pinterest,
            'flickr': flickr,
            'instagram': instagram,
            'soundcloud': soundcloud,
            'visitor_information': visitor_information,
            'start_date': established_date,
            # 'parent': parent,
        }

        # Load
        group, created = self.update_or_create(
            id=mc_pk,
            defaults=defaults,
        )
        return group, created

    def delete_orphans(self, structures):
        # Delete Orphans
        orphans = self.filter(
            id__isnull=False,
        ).exclude(
            id__in=structures,
        )
        t = orphans.count()
        orphans.delete()
        return t

    def sort_tree(self):
        self.all().update(tree_sort=None)
        root = self.get(kind=self.model.KIND.international)
        i = 1
        root.tree_sort = i
        # with disable_auto_indexing(model=self.model):
        #     root.save()
        root.save()
        for child in root.children.order_by('kind', 'code', 'name'):
            i += 1
            child.tree_sort = i
            # with disable_auto_indexing(model=self.model):
            #     child.save()
            child.save()
        orgs = self.filter(
            kind__in=[
                self.model.KIND.district,
                self.model.KIND.noncomp,
                self.model.KIND.chapter,
                self.model.KIND.chorus,
                self.model.KIND.quartet,
            ]
        ).order_by(
            'kind',
            'name',
        )
        for org in orgs:
            i += 1
            org.tree_sort = i
            # with disable_auto_indexing(model=self.model):
            #     org.save()
            org.save()
        return

    # def denormalize(self, cursor=None):
    #     groups = self.filter(status=self.model.STATUS.active)
    #     if cursor:
    #         groups = groups.filter(
    #             modified__gte=cursor,
    #         )
    #     for group in groups:
    #         group.denormalize()
    #         # with disable_auto_indexing(model=self.model):
    #         #     group.save()
    #         group.save()
    #     return

    # def update_seniors(self):
    #     quartets = self.filter(
    #         kind=self.model.KIND.quartet,
    #         status__gt=0,
    #         id__isnull=False,
    #     )

    #     for quartet in quartets:
    #         prior = quartet.is_senior
    #         is_senior = quartet.get_is_senior()
    #         if prior != is_senior:
    #             quartet.is_senior = is_senior
    #             # with disable_auto_indexing(model=self.model):
    #             #     quartet.save()
    #             quartet.save()
    #     return

    def get_quartets(self):
        wb = Workbook()
        ws = wb.active
        fieldnames = [
            'PK',
            'Name',
            'Kind',
            'Organization',
            'District',
            'Chapter(s)',
            'Senior?',
            'BHS ID',
            'Code',
            'Status',
        ]
        ws.append(fieldnames)
        groups = self.filter(
            status=self.model.STATUS.active,
            kind=self.model.KIND.quartet,
        ).order_by('name')
        for group in groups:
            pk = str(group.pk)
            name = group.name
            kind = group.get_kind_display()
            organization = "FIX"
            district = group.district
            chapters = group.chapters
            is_senior = group.is_senior
            is_youth = group.is_youth
            bhs_id = group.bhs_id
            code = group.code
            status = group.get_status_display()
            row = [
                pk,
                name,
                kind,
                organization,
                district,
                chapters,
                is_senior,
                is_youth,
                bhs_id,
                code,
                status,
            ]
            ws.append(row)
        file = save_virtual_workbook(wb)
        content = ContentFile(file)
        return content


class PersonManager(Manager):
    def update_or_create_from_human(self, human):
        # Extract
        if not isinstance(human, dict):
            return ValueError("Must be dictionary")

        mc_pk = human['id']
        first_name = human['first_name']
        middle_name = human['middle_name']
        last_name = human['last_name']
        nick_name = human['nick_name']
        email = human['email']
        birth_date = human['birth_date']
        home_phone = human['home_phone']
        cell_phone = human['cell_phone']
        work_phone = human['work_phone']
        bhs_id = human['bhs_id']
        gender = human['gender']
        part = human['part']
        mon = human['mon']
        is_deceased = human['is_deceased']
        # is_honorary = human['is_honorary']
        # is_suspended = human['is_suspended']
        # is_expelled = human['is_expelled']
        status = human['status']
        current_through = human['current_through']

        _, prefix, first_name = first_name.rpartition('Dr.')
        last_name, suffix, _ = last_name.partition('II')
        last_name, suffix, _ = last_name.partition('II')
        last_name, suffix, _ = last_name.partition('DDS')
        last_name, suffix, _ = last_name.partition('M.D.')
        if last_name.endswith('Sr'):
            last_name, suffix, _ = last_name.partition('Sr')
        if last_name.endswith('Jr'):
            last_name, suffix, _ = last_name.partition('Jr')

        if nick_name == first_name:
            nick_name = ""

        if prefix:
            prefix = prefix.strip()

        first_name.translate(
            first_name.maketrans('', '', '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')
        ).strip()

        last_name.translate(
            last_name.maketrans('', '', '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')
        ).strip()

        if middle_name:
            middle_name.translate(
                middle_name.maketrans('', '', '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')
            ).strip()
        else:
            middle_name = ""

        if nick_name:
            nick_name.translate(
                nick_name.maketrans('', '', '!"#$%&()*+,./:;<=>?@[\\]^_`{|}~')
            ).strip()
        else:
            nick_name = ""

        if suffix:
            suffix = suffix.strip()

        home_phone = validate_phone(home_phone)
        cell_phone = validate_phone(cell_phone)
        work_phone = validate_phone(work_phone)

        email = validate_email(email)

        gender = getattr(self.model.GENDER, gender, None) if gender else None
        part = getattr(self.model.PART, part, None) if part else None

        is_deceased = bool(is_deceased)

        defaults = {
            'status': status,
            'prefix': prefix,
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'suffix': suffix,
            'nick_name': nick_name,
            'email': email,
            'birth_date': birth_date,
            'home_phone': home_phone,
            'cell_phone': cell_phone,
            'work_phone': work_phone,
            'bhs_id': bhs_id,
            'gender': gender,
            'part': part,
            'is_deceased': is_deceased,
            'mon': mon,
            'current_through': current_through,
        }
        # Update or create
        person, created = self.update_or_create(
            id=mc_pk,
            defaults=defaults,
        )
        # Update and create user accounts conditionally:
        if person.email and person.status == person.STATUS.active:
            defaults = {
                'name': person.name,
                'first_name': person.first_name,
                'last_name': person.last_name,
            }
            User.objects.update_or_create(
                email=person.email,
                defaults=defaults,
            )
        person.update_owners()
        return person, created

    def delete_orphans(self, humans):
        # Delete Orphans
        orphans = self.filter(
            id__isnull=False,
        ).exclude(
            id__in=humans,
        )
        t = orphans.count()
        orphans.delete()
        return t

    def export_orphans(self, cursor=None):
        ps = self.filter(
            email__isnull=True,
            user__isnull=False,
        )
        if cursor:
            ps = ps.filter(
                modified__gte=cursor,
            )
        return ps

    def export_adoptions(self, cursor=None):
        ps = self.filter(
            email__isnull=False,
            user__isnull=True,
        )
        if cursor:
            ps = ps.filter(
                modified__gte=cursor,
            )
        return ps


class OfficerManager(Manager):
    def update_or_create_from_role(self, role):
        # Extract
        if not isinstance(role, dict):
            raise RuntimeError("Must be pre-processed")
        # mc_pk = role['id']
        # name = role['name']
        start_date = role['startest_date']
        end_date = role['endest_date']
        person_pk = role['human_id']
        group_pk = role['structure_id']
        status = role['status']

        # Transform
        Person = apps.get_model('bhs.person')
        Group = apps.get_model('bhs.group')

        defaults = {
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
        }

        person = Person.objects.get(id=person_pk)
        group = Group.objects.get(id=group_pk)
        office = self.model.OFFICE.manager

        # Load
        officer, created = self.update_or_create(
            person=person,
            group=group,
            office=office,
            defaults=defaults,
        )
        # Add owners
        group.update_owners()
        return officer, created


    def delete_orphans(self, roles):
        # Delete Orphans
        orphans = self.filter(
            id__isnull=False,
        ).exclude(
            id__in=roles,
        )
        t = orphans.count()
        orphans.delete()
        return t


class MemberManager(Manager):
    def update_or_create_from_join(self, join):
        # Extract
        Person = apps.get_model('bhs.person')
        Group = apps.get_model('bhs.group')
        if not isinstance(join, dict):
            raise RuntimeError("Must be pre-validated")

        # mc_pk = join['id']
        start_date = join['startest_date']
        end_date = join['endest_date']
        vocal_part = join['vocal_part']
        group_pk = join['structure__id']
        person_pk = join['subscription__human__id']
        status = join['status']

        # Transform
        part = getattr(
            self.model.PART,
            vocal_part.strip().lower() if vocal_part else '',
            None,
        )

        # Build dictionary
        defaults = {
            'status': status,
            'start_date': start_date,
            'end_date': end_date,
            'part': part,
        }

        person = Person.objects.get(id=person_pk)
        group = Group.objects.get(id=group_pk)

        # Load
        member, created = self.update_or_create(
            person=person,
            group=group,
            defaults=defaults,
        )
        # Update Person/User conditionally
        # check = all([
        #     member.group.bhs_id == 1, # Only check BHS membership
        #     person.email, # With an email
        #     status > 0, # And currently active status
        # ])
        # if check:
        #     person.current_through = member.end_date
        #     person.status = member.status
        #     person.save()
        #     defaults = {
        #         'name': person.name,
        #         'first_name': person.first_name,
        #         'last_name': person.last_name,
        #     }
        #     user, _ = User.objects.update_or_create(
        #         email=person.email,
        #         defaults=defaults,
        #     )
        #     person.owners.add(user)
        return member, created


    def delete_orphans(self, joins):
        # Delete Orphans
        orphans = self.filter(
            id__isnull=False,
        ).exclude(
            id__in=joins,
        )
        t = orphans.count()
        orphans.delete()
        return t
