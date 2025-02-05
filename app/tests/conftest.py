import pytest

# Fixture for a Person A
@pytest.fixture()
def person_a():
    return {
        "firstname": "Clara",
        "lastname": "Duvall",
        "nickname": "Clary",
    }

# Fixture for a Person B
@pytest.fixture()
def person_b():
    return {
        "firstname": "Peter",
        "lastname": "Smith",
        "nickname": "Pete",
    }

# Fixture for a Person C
@pytest.fixture()
def person_c():
    return {
        "p1_firstname": "Richard",
        "p1_lastname": "Taylor",
        "p1_nickname": "Ricky",
    }

# Fixture for a Person C
@pytest.fixture()
def person_d():
    return {
        "p2_firstname": "Grace",
        "p2_lastname": "Taylor",
        "p2_nickname": "Gracie",
    }

# Fixture for a Person E
@pytest.fixture()
def person_e():
    return {
        "firstname": "Ella",
        "lastname": "Brown",
        "nickname": "Ellie",
    }


