""" main """
from fastapi import FastAPI
from .routers import relationship
from .logging.logger import logger as log
from .data_ingestion.data_importer import DataImporter

app = FastAPI(title='Applicant-screener',
              description='API built for Neo4j with FastAPI',
              version=0.1,
              docs_url='/docs',
              redoc_url='/redoc')

app.include_router(relationship.router)


@app.on_event("startup")
async def startup_event():
    log.info("Starting Neo4j Network creation")
    DataImporter().create_neo4j_network()


@app.get("/")
async def ping():
    return {
        "message": "Hello, we are in home page"
    }
