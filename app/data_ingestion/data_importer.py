import pandas as pd
import yaml
from neo4j import GraphDatabase
from app.utils.db import neo4j_connetion
from app.logging.logger import logger as log

class DataImporter:

    def __init__(self):
        self.yaml_file = r"././data.yml"
        self.conn = neo4j_connetion
        self.dataframe = None
        self.total_nodes = 0
        self.parent_relations = 0
        self.child_relations = 0
        self.friendship = 0

    # Converting yaml to dataframe
    def yaml_to_dataframe(self):
        try:
            with open(self.yaml_file, 'r') as file:
                yaml_data = yaml.safe_load(file)
                self.dataframe = pd.DataFrame(yaml_data['people'])
                log.info(f"Dataframe with {len(self.dataframe.index)} rows, "
                         f"has been created from the yaml file")
        except Exception as e:
            log.error(f"Can't read the yaml file because of {e}")

    # Adds peoples nodes to the Neo4j graph
    def add_people(self):
        log.info(f"Nodes (Persons) creation started")
        query = '''
                UNWIND $rows AS row
                MERGE (p:Person {firstname: row.firstname, lastname: row.lastname,  nickname: row.nickname})
                RETURN count(*) as total
                '''
        try:
            result = self.conn.query(query, parameters={'rows':self.dataframe.to_dict('records')})
            self.total_nodes = result[0]["total"]
            log.info(f"Total nodes number : {self.total_nodes} ")
        except Exception as e:
            log.error(f"Can't create nodes, because of {e}")
        return self.total_nodes

    # Get the nickname from firstname and lastname
    def get_nickname_from_fullname(self, dict_person):
        query='''
            MATCH (n:Person {firstname: $firstname, lastname: $lastname}) RETURN n.nickname as nickname
        '''
        try:
            result = self.conn.query(query, parameters=dict_person)
            if result:
               return result[0]["nickname"]
            else:
               log.info(f"Nickname for Person {dict_person['firstname']}-{dict_person['lastname']} "
                        f"doesn't exist")
        except Exception as e:
            log.error(f"Can't retrieve nickname for Person {dict_person['firstname']}-{dict_person['lastname']}"
                      f"because of {e}")
        return None

    # get childs information of a Person
    def get_childs_fullnames(self, person_dict):
        query = '''
               MATCH (p:Person)-[:CHILD_OF]->(c:Person) 
               WHERE c.firstname = $firstname AND  c.lastname = $lastname AND c.nickname = $nickname
               RETURN p.firstname as firstname, p.nickname as nickname, p.lastname as lastname
        '''
        try:
            result = self.conn.query(query, parameters=person_dict)
            return result
        except Exception as e:
            log.error(f"Can't retrieve child of Person {person_dict['firstname']}-{person_dict['lastname']}"
                      f"because of {e}")

    def add_child_relations(self):
       log.info(f"IS_CHILD relationships creation started")
       childs_dataframe = self.dataframe[(self.dataframe['child_of'].notna()) & (self.dataframe['child_of'].str.len() != 0)]
       childs_rows = childs_dataframe.to_dict('records')
       for row in childs_rows:
           person_dict = {}
           person_dict["p_firstname"] = row['firstname']
           person_dict["p_lastname"] = row['lastname']
           person_dict["p_nickname"] = row['nickname']
           person_dict["parent_firstname"] = row['child_of'][0].split()[0]
           person_dict["parent_lastname"] = row['child_of'][0].split()[1]
           person_dict["parent_nickname"] = self.get_nickname_from_fullname(
               {"firstname": person_dict["parent_firstname"],
                "lastname": person_dict["parent_lastname"]}
           )
           query = '''
           MERGE (p:Person {firstname : $p_firstname, lastname : $p_lastname, nickname: $p_nickname}) 
           MERGE (c:Person {firstname : $parent_firstname, lastname : $parent_lastname, nickname: $parent_nickname}) 
           // connect People
           MERGE (p)-[:CHILD_OF]->(c)
           '''
           try:
               self.conn.query(query, parameters=person_dict)
               self.child_relations += 1
           except Exception as e:
               log.error(f"Can't create IS_CHILD relationship between : "
                         f"Person: {person_dict['p_firstname']}-{person_dict['p_lastname']} "
                         f"and Parent: {person_dict['parent_firstname']}-{person_dict['parent_lastname']}"
                         f"because of {e}")
       log.info(f"Total number of IS_CHILD relationships : {self.child_relations}")
       return self.child_relations

    def add_parent_relations(self):
       log.info(f"PARENT_OF relationships creation started")
       parents_rows = self.dataframe[(self.dataframe['parent_of'].notna()) & (self.dataframe['parent_of'].str.len() != 0)]
       parents_rows = parents_rows.to_dict('records')
       for row in parents_rows:
           person_dict = {}
           person_dict['p_firstname'] = row['firstname']
           person_dict['p_lastname'] = row['lastname']
           person_dict['p_nickname'] = row['nickname']
           list_of_childs = row['parent_of']
           for child in list_of_childs:
               if len(child.split()) == 2:
                   person_dict['child_firstname'] = child.split()[0]
                   person_dict['child_lastname'] = child.split()[1]
                   person_dict['child_nickname'] = self.get_nickname_from_fullname(
                       {"firstname": person_dict["child_firstname"],
                        "lastname": person_dict["child_lastname"]}
                   )
                   query = '''
                        MERGE (p:Person {firstname : $p_firstname, lastname : $p_lastname, nickname: $p_nickname}) 
                        MERGE (c:Person {firstname : $child_firstname, lastname : $child_lastname, nickname: $child_nickname}) 
                        // connect People
                        MERGE (p)-[:PARENT_OF]->(c)
                        '''
                   try:
                       self.conn.query(query, parameters=person_dict)
                       self.parent_relations += 1
                   except Exception as e:
                       log.error(f"Can't create IS_CHILD relationship between : "
                            f"Person: {person_dict['p_firstname']}-{person_dict['p_lastname']} "
                            f"and CHILD: {person_dict['child_firstname']}-{person_dict['child_lastname']}"
                            f"because of {e}")

               else:
                   childs = self.get_childs_fullnames(
                       {"firstname": person_dict["p_firstname"],
                        "lastname": person_dict["p_lastname"],
                        "nickname": person_dict["p_nickname"],
                        }
                   )
                   for child in childs :
                       person_dict['child_firstname'] = child['firstname']
                       person_dict['child_lastname'] = child['lastname']
                       person_dict['child_nickname'] = child['nickname']
                       query = '''
                       MERGE (p:Person {firstname : $p_firstname, lastname : $p_lastname, nickname: $p_nickname}) 
                       MERGE (c:Person {firstname : $child_firstname, lastname : $child_lastname, nickname: $child_nickname}) 
                       // connect People
                       MERGE (p)-[:PARENT_OF]->(c)
                       '''
                       try:
                           self.conn.query(query, parameters=person_dict)
                           self.parent_relations += 1
                       except Exception as e:
                           log.error(f"Can't create IS_CHILD relationship between : "
                             f"Person: {person_dict['p_firstname']}-{person_dict['p_lastname']} "
                             f"and CHILD: {person_dict['child_firstname']}-{person_dict['child_lastname']}"
                             f"because of {e}")

       log.info(f"Total number of PARENT_OF relationships : {self.parent_relations}")
       return self.parent_relations

    def add_friendship(self):
       log.info(f"friendships creation started")
       friends_rows = self.dataframe[(self.dataframe['friend_of'].notna()) & (self.dataframe['friend_of'].str.len() != 0)]
       friends_rows = friends_rows.to_dict('records')
       for row in friends_rows:
           dict_person = {}
           dict_person['p_firstname'] = row['firstname']
           dict_person['p_lastname'] = row['lastname']
           dict_person['p_nickname'] = row['nickname']
           list_of_friends = row['friend_of']
           for friend in list_of_friends:
                   dict_person['friend_firstname'] = friend.split()[0]
                   dict_person['friend_lastname'] = friend.split()[1]
                   dict_person['friend_nickname'] = self.get_nickname_from_fullname(
                        {"firstname": dict_person["friend_firstname"],
                        "lastname": dict_person["friend_lastname"]}
                   )
                   query = '''
                        MERGE (p:Person {firstname : $p_firstname, lastname : $p_lastname, nickname: $p_nickname}) 
                        MERGE (c:Person {firstname : $friend_firstname, lastname : $friend_lastname, nickname: $friend_nickname}) 
                        // connect Friends
                        MERGE (p)-[:FRIEND_OF]-(c)
                        '''
                   try:
                       self.conn.query(query, parameters=dict_person)
                       log.info(f"Friendship created between :"
                       f"Person: {dict_person['p_firstname']}-{dict_person['p_lastname']} "
                       f"and Friend: {dict_person['friend_firstname']}-{dict_person['friend_lastname']}")
                       self.friendship += 1
                   except Exception as e:
                       log.error(f"Can't create friendship between : "
                                 f"Person: {dict_person['p_firstname']}-{dict_person['p_lastname']} "
                                 f"and Friend: {dict_person['friend_firstname']}-{dict_person['friend_lastname']}"
                                 f"because of {e}")
       log.info(f"Total number of friendships : {self.friendship}")
       return self.friendship

    def create_neo4j_network(self):
        self.yaml_to_dataframe()
        self.add_people()
        self.add_child_relations()
        self.add_parent_relations()
        self.add_friendship()
        self.conn.close()
        return True



