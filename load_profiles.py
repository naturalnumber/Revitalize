import Revitalize.models

# To load this run:
# python ./manage.py shell
# Then enter:
# exec(open("./load_profiles.py").read())

# not fully tested for fresh install, may need minor adjustments

debug = False

profile1 = {
        "user": 2,
        "first_name": "One",
        "middle_name": "Test",
        "last_name": "A",
        "date_of_birth": "1901-01-11",
        "gender": "M",
        "phone_number": "9021111111",
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
        "ec_phone_number": "9021110000",
        "physician": "TestOnePhysician",
        "points": 0,
        "personal_message": "PersonalMessageOne",
        "profile_picture": "null",
        "password_flag": "True",
        "preferences": "{}",
        "id": 2
}


profile2 = {
        "user": 3,
        "first_name": "Two",
        "middle_name": "Test",
        "last_name": "B",
        "date_of_birth": "1902-02-22",
        "gender": "F",
        "phone_number": "9022222222",
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
        "preferences": "{}",
        "id": 3
}


profile3 = {
        "user": 4,
        "first_name": "Three",
        "middle_name": "Test",
        "last_name": "C",
        "date_of_birth": "1903-03-03",
        "gender": "M",
        "phone_number": "9023333333",
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
        "preferences": "{}",
        "id": 4
}


profile4 = {
        "user": 5,
        "first_name": "Four",
        "middle_name": "Test",
        "last_name": "D",
        "date_of_birth": "1904-04-04",
        "gender": "O",
        "phone_number": "9024444444",
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
        "preferences": "{}",
        "id": 5
}


profile5 = {
        "user": 6,
        "first_name": "Five",
        "middle_name": "Test",
        "last_name": "E",
        "date_of_birth": "1905-05-05",
        "gender": "F",
        "phone_number": "9025555555",
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
        "preferences": "{}",
        "id": 6
}

profile_list = [profile1, profile2, profile3, profile4, profile5]


def load_profiles(p: dict):

    profile = Revitalize.models.Profile.objects.create(
            user_id=p.__getitem__('user'),
            first_name=p.__getitem__('first_name'),
            middle_name=p.__getitem__('middle_name'),
            last_name=p.__getitem__('last_name'),
            date_of_birth=p.__getitem__('date_of_birth'),
            gender=p.__getitem__('gender'),
            phone_number=p.__getitem__('phone_number'),
            phone_number_alt=p.__getitem__('phone_number_alt'),
            email=p.__getitem__('email'),
            street_address=p.__getitem__('street_address'),
            city=p.__getitem__('city'),
            province=p.__getitem__('province'),
            country=p.__getitem__('country'),
            postal_code=p.__getitem__('postal_code'),
            ec_first_name=p.__getitem__('ec_first_name'),
            ec_middle_name=p.__getitem__('ec_middle_name'),
            ec_last_name=p.__getitem__('ec_last_name'),
            ec_phone_number=p.__getitem__('ec_phone_number'),
            physician=p.__getitem__('physician'),
            points=p.__getitem__('points'),
            personal_message=p.__getitem__('personal_message'),
            profile_picture=p.__getitem__('profile_picture'),
            password_flag=p.__getitem__('password_flag'),
            preferences=p.__getitem__('preferences'),
            id=p.__getitem__('id'),
    )

    print(f"created: {profile}")


loaded = [load_profiles(p) for p in profile_list]

# python ./manage.py shell
# exec(open("./load_profiles.py").read())
