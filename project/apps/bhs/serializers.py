
# Third-Party
from dry_rest_permissions.generics import DRYPermissionsField
from rest_framework.serializers import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator
# from rest_framework_json_api import serializers
from rest_framework import serializers
from rest_framework_json_api.relations import ResourceRelatedField
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.core.validators import validate_email

from phonenumber_field.validators import validate_international_phonenumber
# Local
from .fields import TimezoneField
from .models import Group
from .models import Member
from .models import Officer
from .models import Person

User = get_user_model()
validate_url = URLValidator()

class GroupSerializer(serializers.ModelSerializer):
    # permissions = DRYPermissionsField()
    included_serializers = {
        # 'repertories': 'apps.bhs.serializers.RepertorySerializer',
        # 'members': 'apps.bhs.serializers.MemberSerializer',
        # 'officers': 'apps.bhs.serializers.OfficerSerializer',
    }

    AIC = {
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

    KIND = {
        'quartet': Group.KIND.quartet,
        'chorus': Group.KIND.chorus,
        'chapter': Group.KIND.chapter,
        'group': Group.KIND.noncomp,
        'district': Group.KIND.district,
        'organization': Group.KIND.international,
    }

    GENDER = {
        'men': Group.GENDER.male,
        'women': Group.GENDER.female,
        'mixed': Group.GENDER.mixed,
    }

    DIVISION = {
        'EVG Division I': Group.DIVISION.evgd1,
        'EVG Division II': Group.DIVISION.evgd2,
        'EVG Division III': Group.DIVISION.evgd3,
        'EVG Division IV': Group.DIVISION.evgd4,
        'EVG Division V': Group.DIVISION.evgd5,
        'FWD Arizona': Group.DIVISION.fwdaz,
        'FWD Northeast': Group.DIVISION.fwdne,
        'FWD Northwest': Group.DIVISION.fwdnw,
        'FWD Southeast': Group.DIVISION.fwdse,
        'FWD Southwest': Group.DIVISION.fwdsw,
        'LOL 10000 Lakes': Group.DIVISION.lol10l,
        'LOL Division One': Group.DIVISION.lolone,
        'LOL Northern Plains': Group.DIVISION.lolnp,
        'LOL Packerland': Group.DIVISION.lolpkr,
        'LOL Southwest': Group.DIVISION.lolsw,
        'MAD Central': Group.DIVISION.madcen,
        'MAD Northern': Group.DIVISION.madnth,
        'MAD Southern': Group.DIVISION.madsth,
        'NED Granite and Pine': Group.DIVISION.nedgp,
        'NED Mountain': Group.DIVISION.nedmtn,
        'NED Patriot': Group.DIVISION.nedpat,
        'NED Sunrise': Group.DIVISION.nedsun,
        'NED Yankee': Group.DIVISION.nedyke,
        'SWD Northeast': Group.DIVISION.swdne,
        'SWD Northwest': Group.DIVISION.swdnw,
        'SWD Southeast': Group.DIVISION.swdse,
        'SWD Southwest': Group.DIVISION.swdsw,
    }

    STATUS = {
        '64ad817f-f3c6-4b09-a1b0-4bd569b15d03': Group.STATUS.inactive, # revoked
        'd9e3e257-9eca-4cbf-959f-149cca968349': Group.STATUS.inactive, # suspended
        '6e3c5cc6-0734-4edf-8f51-40d3a865a94f': Group.STATUS.inactive, # merged
        'bd4721e7-addd-4854-9888-8a705725f748': Group.STATUS.inactive, # closed
        'e04744e6-b743-4247-92c2-2950855b3a93': Group.STATUS.inactive, # expired
        '55a97973-02c3-414a-bbef-22181ad46e85': Group.STATUS.active, # pending
        'bb1ee6f6-a2c5-4615-b6ad-76130c37b1e6': Group.STATUS.active, # pending voluntary
        'd7102af8-013a-40e7-bc85-0b00766ed124': Group.STATUS.active, # awaiting
        'f3facc00-1990-4c68-9052-39e066906a38': Group.STATUS.active, # prospective
        '4bfee76f-3110-4c32-bade-e5044fdd5fa2': Group.STATUS.active, # licensed
        '7b9e5e34-a7c5-4f1e-9fc5-656caa74b3c7': Group.STATUS.active, # active
    }

    def validate_name(self, name):
        if name in self.AIC.values():
            raise ValidationError("Can not choose name of AIC member")
        return name

    def validate_status(self, status):
        status = self.STATUS.get(status, None)
        if not status:
            raise self.ValidationError("Status not specified.")
        return status

    def validate_kind(self, kind):
        kind = self.KIND.get(kind, None)
        if not kind:
            raise self.ValidationError("Kind not specified.")
        return kind

    def validate_gender(self, gender):
        gender = self.GENDER.get(gender, None)
        if not gender:
            raise ValidationError("Gender not specified.")

    def validate_district(self, district):
        return district

    def validate_division(self, division):
        division = self.DIVISION.get(division, None)
        if not division:
            raise ValidationError("Division not specified.")

    def validate_bhs_id(self, bhs_id):
        return bhs_id

    def validate_code(self, code):
        return code

    def validate_website(self, website):
        if website:
            return validate_url(website)
        return ''

    def validate_email(self, email):
        if email:
            return validate_email(email)
        return ''

    def validate_phone(self, phone):
        if phone:
            return validate_international_phonenumber(phone)
        return ''

    def validate_fax_phone(self, fax_phone):
        if fax_phone:
            return validate_international_phonenumber(fax_phone)
        return ''

    def validate_start_date(self, start_date):
        return start_date

    def validate_end_date(self, end_date):
        return end_date

    def validate_facebook(self, facebook):
        if facebook:
            return validate_url(facebook)
        return ''

    def validate_twitter(self, twitter):
        if twitter:
            return validate_url(twitter)
        return ''

    def validate_youtube(self, youtube):
        if youtube:
            return validate_url(youtube)
        return ''

    def validate_pinterest(self, pinterest):
        if pinterest:
            return validate_url(pinterest)
        return ''

    def validate_flickr(self, flickr):
        if flickr:
            return validate_url(flickr)
        return ''

    def validate_instagram(self, instagram):
        if instagram:
            return validate_url(instagram)
        return ''

    def validate_soundcloud(self, soundcloud):
        if soundcloud:
            return validate_url(soundcloud)
        return ''

    def validate_visitor_information(self, visitor_information):
        return visitor_information.strip() if visitor_information else ''


    class Meta:
        model = Group
        fields = [
            'id',
            # 'name',
            # 'status',
            # 'kind',
            # 'gender',
            # 'district',
            # 'division',
            # 'bhs_id',
            # 'code',
            # 'website',
            # 'email',
            # 'phone',
            # 'fax_phone',
            # 'start_date',
            # 'end_date',
            # 'location',
            # 'facebook',
            # 'twitter',
            # 'youtube',
            # 'pinterest',
            # 'flickr',
            # 'instagram',
            # 'soundcloud',
            # 'image',
            # 'description',
            # 'visitor_information',
            # 'participants',
            # 'chapters',
            # 'notes',
            # 'tree_sort',

            # 'is_senior',
            # 'is_youth',

            # 'owners',
            # 'parent',
            # # 'children',

            # # 'repertories',
            # 'permissions',
            # 'usernames',

            # 'nomen',
            # 'image_id',
            # 'created',
            # 'modified',
        ]

        read_only_fields = [
            'nomen',
            'usernames',
            'image_id',
            'created',
            'modified',
        ]

    class JSONAPIMeta:
        included_resources = [
            # 'repertories',
            # 'members',
            # 'officers',
        ]

    # def to_representation(self, instance):
    #     if instance.kind <= 30:
    #         self.fields.pop('members')
    #     return super().to_representation(instance)


class MemberSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Member
        fields = [
            'id',
            'status',
            'part',
            'start_date',
            'end_date',
            'group',
            'person',
            'permissions',
        ]


class OfficerSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()

    class Meta:
        model = Officer
        fields = [
            'id',
            'status',
            'start_date',
            'end_date',
            'office',
            'person',
            'group',
            'permissions',
        ]

        validators = [
            UniqueTogetherValidator(
                queryset=Officer.objects.all(),
                fields=('person', 'office'),
                message='This person already holds this office.',
            )
        ]


class PersonSerializer(serializers.ModelSerializer):
    permissions = DRYPermissionsField()
    owners = ResourceRelatedField(
        many=True,
        read_only=True,
    )
    # included_serializers = {
    #     'owners': 'rest_framework_jwt.serializers.UserSerializer',
    #     # 'members': 'apps.bhs.serializers.MemberSerializer',
    #     # 'officers': 'apps.bhs.serializers.OfficerSerializer',
    # }



    class Meta:
        model = Person
        fields = [
            'id',
            'status',
            'prefix',
            'first_name',
            'middle_name',
            'last_name',
            'nick_name',
            'suffix',
            'birth_date',
            'spouse',
            'location',
            'part',
            'mon',
            'gender',
            'is_deceased',
            'is_honorary',
            'is_suspended',
            'is_expelled',
            'email',
            'address',
            'home_phone',
            'work_phone',
            'cell_phone',
            'airports',
            'image',
            'description',
            'notes',
            'bhs_id',

            'nomen',
            'name',
            'full_name',
            'common_name',
            'sort_name',
            'initials',
            'image_id',
            'owners',
            'current_through',

            # 'current_status',
            # 'current_district',

            # 'owners',
            'usernames',
            'permissions',
            'created',
            'modified',
        ]
        read_only_fields = [
            'nomen',
            'name',
            'full_name',
            'common_name',
            'sort_name',
            'initials',
            'image_id',
            'usernames',
            # 'current_through',
            # 'current_status',
            # 'current_district',
            'created',
            'modified',
        ]
    class JSONAPIMeta:
        included_resources = [
            # 'owners',
            # 'members',
            # 'officers',
        ]