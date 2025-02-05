from fastapi import APIRouter, Request
from app.utils.db import neo4j_connetion
from app.schemas.nodes import Person
from app.logging.logger import logger as log
from app.data_ingestion.data_importer import  DataImporter
import json

router = APIRouter(
    prefix='/relationship',
    tags = ['relationship']
)

# Get all ancestors of a person
@router.get(
    "/get_all_ancestors",
    response_model=list[Person],
    response_description="Get all ancestors of a person",
)
async def get_all_ancestors(request: Request):
    log.info("/get_all_ancestors Started")
    params = request.query_params
    query = '''
           MATCH (p:Person)-[:PARENT_OF*2..]->(c:Person) 
           WHERE c.firstname = $firstname AND  c.lastname = $lastname AND c.nickname = $nickname
           RETURN p.firstname as firstname, p.nickname as nickname, p.lastname as lastname
    '''
    result = neo4j_connetion.query(query, parameters=params)
    if result:
        result = list({person['firstname']:person for person in result}.values())
        log.info(f"List of ancestors of Person: {params['firstname']}-{params['lastname']}, is: {result}")
    neo4j_connetion.close()
    return result


# Get all friends of family members of a person
@router.get(
    "/get_family_friends",
    response_model=list[Person],
    response_description="Get all friends of family members",
)
async def get_all_family_friends(request: Request):
    log.info("/get_all_family_friends Started")
    params = request.query_params
    query = '''
           MATCH (f:Person)-[:FRIEND_OF]-(p:Person)-[:PARENT_OF|CHILD_OF]->(c:Person)
           WHERE c.firstname = $firstname AND  c.lastname = $lastname AND c.nickname = $nickname
           RETURN f.firstname as firstname, f.nickname as nickname, f.lastname as lastname
    '''
    result = neo4j_connetion.query(query, parameters=params)
    if result:
        result = list({person['firstname']:person for person in result}.values())
        log.info(f"List of all family friends of Person: {params['firstname']}-{params['lastname']}, is: {result}")
    neo4j_connetion.close()
    return result


# Get family members of a person
@router.get(
    "/get_family",
    response_model=list[Person],
    response_description="Get all family members",
)
async def get_family(request: Request):
    log.info("/get_family Started")
    params = request.query_params
    query = '''
           MATCH (p:Person)-[:PARENT_OF|CHILD_OF]->(c:Person)
           WHERE c.firstname = $firstname AND  c.lastname = $lastname AND c.nickname = $nickname
           RETURN p.firstname as firstname, p.nickname as nickname, p.lastname as lastname
    '''
    result = neo4j_connetion.query(query, parameters=params)
    if result:
        result = list({person['firstname']:person for person in result}.values())
        log.info(f"List of all family of Person: {params['firstname']}-{params['lastname']}, is: {result}")
    neo4j_connetion.close()
    return result


# Get all relationships between two persons p1 and p2
@router.get("/get_relationships")
async def get_relationships(request: Request):
    log.info("/get_relationships Started")
    params = request.query_params
    log.info(params)
    query = '''
           MATCH (p:Person)-[r]->(c:Person)
           WHERE p.firstname = $p1_firstname AND  p.lastname = $p1_lastname AND p.nickname = $p1_nickname
           AND c.firstname = $p2_firstname AND  c.lastname = $p2_lastname AND c.nickname = $p2_nickname
           RETURN r as relation
    '''
    relations = neo4j_connetion.query(query, parameters=params)
    list_of_relations = []
    for relation in relations:
        list_of_relations.append(relation['relation'][1])
    log.info(f"List relationships between "
             f"Person1: {params['p1_firstname']}-{params['p1_lastname']} "
             f"and Person2: {params['p2_firstname']}-{params['p2_lastname']}, "
             f"is : {list_of_relations}")
    return list_of_relations


# Get childs fullnames of a person
@router.get(
    "/get_childs_fullnames",
    response_model=list[Person],
    response_description="Get childs fullnames",
)
async def get_childs_fullnames(request: Request):
    log.info("/get_childs_fullnames Started")
    params = request.query_params
    data_importer = DataImporter()
    result = data_importer.get_childs_fullnames(params)
    neo4j_connetion.close()
    log.info(f"List of childs for Person: {params['firstname']}-{params['lastname']}, is: {result}")
    return result


# Create new person
@router.post(
    "/add_person",
    response_model=Person,
    response_description="Add new person",
)
async def add_person(person):
    log.info("/add_person Started")
    log.info(person)
    params = json.loads(person)
    query = '''
        MERGE (p:Person {firstname: $firstname, lastname: $lastname,  nickname: $nickname})
        RETURN p.firstname as firstname, p.lastname as lastname, p.nickname as nickname
    '''
    result = neo4j_connetion.query(query, parameters=params)
    if result:
        log.info(f"Adding person : {params['firstname']}-{params['lastname']} is done")
        neo4j_connetion.close()
        return result[0]
    else:
       log.info(f"Couldn't create a node for Person: {params}")
       return {"firstname":"", "lastname":"", "nickname":""}


# Adding friendship
@router.post(
    "/create_friendship",
    response_description="Adding friendship relation",
)
async def create_friendship(persons):
    log.info("/create_friendship Started")
    log.info(persons)
    params = json.loads(persons)
    log.info(params)
    query = '''
        MERGE (p:Person {firstname : $p_firstname, lastname : $p_lastname, nickname: $p_nickname}) 
        MERGE (c:Person {firstname : $friend_firstname, lastname : $friend_lastname, nickname: $friend_nickname}) 
        MERGE (p)-[:FRIEND_OF]-(c)
        RETURN true
    '''
    result = neo4j_connetion.query(query, parameters=params)
    if result:
        log.info(f"Friendship created between :"
        f"Person: {params['p_firstname']}-{params['p_lastname']} "
        f"and Friend: {params['friend_firstname']}-{params['friend_lastname']}")
        neo4j_connetion.close()
        return True
    else:
       log.info(f"Couldn't create friendship relation between People: {params}")
       return False
