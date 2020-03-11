import Revitalize.models as models
from Revitalize.models import Profile, Address, CanadianAddress
from django.contrib.auth import get_user_model

# To load this run:
# python ./manage.py shell
# Then enter:
# exec(open("./load_profiles.py").read())

# not fully tested for fresh install, may need minor adjustments

debug = False

profile0 = {
        "user": 1,
        "first_name": "Adisson",
        "middle_name": "Dorothy",
        "last_name": "Ministrator",
        "date_of_birth": "1971-09-17",
        "gender": "F",
        "phone_number": "9025550000",
        "phone_number_alt": "",
        "email": "admin@test.com",
        "street_address": "123 Fake St.",
        "city": "Charlottetown",
        "province": "PE",
        "country": "Canada",
        "postal_code": "C1A9A9",
        "ec_first_name": "Emily",
        "ec_middle_name": "Erica",
        "ec_last_name": "Gency",
        "ec_phone_number": "9025550000",
        "physician": "TestOnePhysician",
        "points": 0,
        "personal_message": "Personal Message Admin",
        "profile_picture": "null",
        "password_flag": "True",
        "preferences": "{}"
}

profile1 = {
        "user": 2,
        "first_name": "One",
        "middle_name": "Test",
        "last_name": "A",
        "date_of_birth": "1901-01-11",
        "gender": "M",
        "phone_number": "9025550011",
        "phone_number_alt": "",
        "email": "one@test.com",
        "street_address": "StreetOne",
        "city": "CityOne",
        "province": "ProvinceOne",
        "country": "CountryOne",
        "postal_code": "A1A1A1",
        "ec_first_name": "ecOneF",
        "ec_middle_name": "ecMid",
        "ec_last_name": "ecLast",
        "ec_phone_number": "9025550000",
        "physician": "TestOnePhysician",
        "points": 0,
        "personal_message": "PersonalMessageOne",
        "profile_picture": "null",
        "password_flag": "True",
        "preferences": "{}"
}


profile2 = {
        "user": 3,
        "first_name": "Two",
        "middle_name": "Test",
        "last_name": "B",
        "date_of_birth": "1902-02-22",
        "gender": "F",
        "phone_number": "9025550022",
        "phone_number_alt": "",
        "email": "two@test.com",
        "street_address": "StreetTwo",
        "city": "CityTwo",
        "province": "ProvinceTwo",
        "country": "CountryTwo",
        "postal_code": "B2B2B2",
        "ec_first_name": "ecTwoF",
        "ec_middle_name": "ecMid",
        "ec_last_name": "ecLast",
        "ec_phone_number": "9022220000",
        "physician": "TestTwoPhysician",
        "points": 0,
        "personal_message": "PersonalMessageTwo",
        "profile_picture": "null",
        "password_flag": "True",
        "preferences": "{}"
}


profile3 = {
        "user": 4,
        "first_name": "Three",
        "middle_name": "Test",
        "last_name": "C",
        "date_of_birth": "1903-03-03",
        "gender": "M",
        "phone_number": "9025550033",
        "phone_number_alt": "",
        "email": "three@test.com",
        "street_address": "StreetThree",
        "city": "CityThree",
        "province": "ProvinceThree",
        "country": "CountryThree",
        "postal_code": "C3C3C3",
        "ec_first_name": "ecThreeF",
        "ec_middle_name": "ecMid",
        "ec_last_name": "ecLast",
        "ec_phone_number": "9023330000",
        "physician": "TestThreePhysician",
        "points": 0,
        "personal_message": "PersonalMessageThree",
        "profile_picture": "null",
        "password_flag": "True",
        "preferences": "{}"
}


profile4 = {
        "user": 5,
        "first_name": "Four",
        "middle_name": "Test",
        "last_name": "D",
        "date_of_birth": "1904-04-04",
        "gender": "O",
        "phone_number": "9025550044",
        "phone_number_alt": "",
        "email": "four@test.com",
        "street_address": "StreetFour",
        "city": "CityFour",
        "province": "ProvinceFour",
        "country": "CountryFour",
        "postal_code": "D4D4D4",
        "ec_first_name": "ecFourF",
        "ec_middle_name": "ecMid",
        "ec_last_name": "ecLast",
        "ec_phone_number": "9024440000",
        "physician": "TestFourPhysician",
        "points": 0,
        "personal_message": "PersonalMessageFour",
        "profile_picture": "null",
        "password_flag": "True",
        "preferences": "{}"
}


profile5 = {
        "user": 6,
        "first_name": "Five",
        "middle_name": "Test",
        "last_name": "E",
        "date_of_birth": "1905-05-05",
        "gender": "F",
        "phone_number": "9025550055",
        "phone_number_alt": "",
        "email": "five@test.com",
        "street_address": "StreetFive",
        "city": "CityFive",
        "province": "ProvinceFive",
        "country": "CountryFive",
        "postal_code": "E5E5E5",
        "ec_first_name": "ecFiveF",
        "ec_middle_name": "ecMid",
        "ec_last_name": "ecLast",
        "ec_phone_number": "9025550000",
        "physician": "TestFivePhysician",
        "points": 0,
        "personal_message": "PersonalMessageFive",
        "profile_picture": "null",
        "password_flag": "True",
        "preferences": "{}"
}

profile_list = [profile0, profile1, profile2, profile3, profile4, profile5]


def load_profiles(p: dict):
    User = get_user_model()

    try:
        user = User.objects.get(pk=p['user'])
    except:
        user = User.objects.create_superuser(p['first_name'], '', 'cs4820')

    print(f"trying to make: {p['first_name']}")
    
    address_base = Address.objects.create(country=Address.Country.CANADA)
    address = CanadianAddress.objects.create(base=address_base,
                                             street_address=p['street_address'],
                                             city=p['city'],
                                             postal_code=p['postal_code'],
                                             province=CanadianAddress.Province.PRINCE_EDWARD_ISLAND)

    profile = Profile.objects.create(
            address=address_base,
            user_id=p['user'],
            first_name=p['first_name'],
            middle_name=p['middle_name'],
            last_name=p['last_name'],
            date_of_birth=p['date_of_birth'],
            gender=p['gender'],
            phone_number=p['phone_number'],
            phone_number_alt=p['phone_number_alt'],
            email=p['email'],
            ec_first_name=p['ec_first_name'],
            ec_middle_name=p['ec_middle_name'],
            ec_last_name=p['ec_last_name'],
            ec_phone_number=p['ec_phone_number'],
            physician=p['physician'],
            points=p['points'],
            personal_message=p['personal_message'],
            profile_picture=p['profile_picture'],
            password_flag=p['password_flag'],
            preferences=p['preferences'],
    )

    print(f"created: {profile}")


loaded = [load_profiles(p) for p in profile_list]

# python ./manage.py shell
# exec(open("./load_profiles.py").read())
