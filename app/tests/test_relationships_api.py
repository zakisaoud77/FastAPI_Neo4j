from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def sort_persons(list_persons):
   return sorted(list_persons, key=lambda p: (p['nickname'], p['firstname'], p['nickname']))

def test_get_childs_fullnames(person_a):
    response = client.get(
        "relationship/get_childs_fullnames",
        params=person_a
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert sort_persons(response.json()) == sort_persons(
        [{"firstname":"Mary","lastname":"Smith","nickname":"M&M"},
         {"firstname":"Peter","lastname":"Smith","nickname":"Pete"}]
    )


def test_get_family_friends(person_b):
    response = client.get(
        "relationship/get_family_friends",
        params=person_b
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert sort_persons(response.json()) == sort_persons(
        [{"firstname":"Rachel","lastname":"Brown","nickname":"Ray"},
         {"firstname":"Olivia","lastname":"Brown","nickname":"Liv"}]
    )


def test_get_relationships(person_c, person_d):
    person_c.update(person_d)
    response = client.get(
        "relationship/get_relationships",
        params=person_c
    )
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json() == ["CHILD_OF","FRIEND_OF"]


def test_get_family(person_e):
    response = client.get(
        "relationship/get_family",
        params=person_e
    )
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert sort_persons(response.json()) == sort_persons(
        [{"firstname":"Sara","lastname":"Brown","nickname":"Sar"},
         {"firstname":"Ian","lastname":"Brown","nickname":"E"},
         {"firstname":"James","lastname":"Brown","nickname":"Jimbo"}]
    )


def test_get_all_ancestors(person_b):
    response = client.get(
        "relationship/get_all_ancestors",
        params=person_b
    )
    assert response.status_code == 200
    assert len(response.json()) == 5
    assert sort_persons(response.json()) == sort_persons(
        [{"firstname":"John","lastname":"Smith","nickname":"Johnny"},
         {"firstname":"Anna","lastname":"Smith","nickname":"Annie"},
         {"firstname":"Lisa","lastname":"Smith","nickname":"Lee"},
         {"firstname":"Tom","lastname":"Smith","nickname":"Tommy"},
         {"firstname":"Victor","lastname":"Smith","nickname":"Vic"}]
    )


def test_create_friendship():
    response = client.post(
        "relationship/create_friendship",
        params = {"persons" :"""{"p_firstname":"Zakaria","p_lastname":"SAOUD","p_nickname":"Zack",
                   "friend_firstname": "Kamel", "friend_lastname": 
                   "Kamel","friend_nickname": "Koko"}"""}
    )
    assert response.status_code == 200

    response = client.get(
        "relationship/get_relationships",
        params={"p1_firstname":"Zakaria","p1_lastname":"SAOUD","p1_nickname":"Zack",
                "p2_firstname": "Kamel", "p2_lastname": "Kamel","p2_nickname": "Koko"}
    )
    assert response.status_code == 200
    assert response.json() == ["FRIEND_OF"]

