from neo4j import GraphDatabase
from app.utils.environment import Config
from app.logging.logger import logger as log

class Neo4jDatabaseConnection:

    def __init__(self, uri, user, pwd):
        self.db_uri = uri
        self.db_user = user
        self.db_pwd = pwd
        self.db_driver = None
        try:
            self.db_driver = GraphDatabase.driver(self.db_uri, auth=(self.db_user, self.db_pwd))
        except Exception as e:
            log.error("Failed to create the driver:", e)

    def test_connectivity(self):
        if self.db_driver:
            self.db_driver.verify_connectivity()
            log.info("Connection estabilished.")
            return True

    def close(self):
        if self.db_driver is not None:
            self.db_driver.close()

    def query(self, query, parameters=None, db=None):
        assert self.db_driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = self.db_driver.session(database=db) if db is not None else self.db_driver.session()
            response = session.run(query, parameters).data()
        except Exception as e:
            log.error(f"Query failed: because of {e}")
        finally:
            if session is not None:
                session.close()
        return response

neo4j_connetion = Neo4jDatabaseConnection(
        uri=Config.NEO4J_URI,
        user=Config.NEO4J_USERNAME,
        pwd=Config.NEO4J_PASSWORD
)
