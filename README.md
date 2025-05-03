# Social Network with Fastapi and Neo4j

## Goal

The goal of this project is to build the prototype of an API for a social network that will be able to manage any number of People and capture different types of relationships between them

For each People the system will record 3 informations
- First name
- Last name
- Nickname (Optional)

Between 2 People the system is be able to capture two types of relationships
- Friendship information (a friendship will automatically be bi-directional)
- Family information (parent, kid)

In additional to the CRUD endpoints required to manage People and their relationships, the system can expose 2 API to query information
- Query all ancestors for a given person
- Query all family’s friends of any given person. (family’s friend is defined as someone who’s friend with any member of your family)

## Technical Stack

- FastAPI is used for the web server
- Neo4j is used for the database

## Resource Available

A docker compose can be used to start a local docker container, otherwise it's possible to use a free Cloud instance of Neo4j in the Cloud https://neo4j.com/cloud/platform/aura-graph-database/

## Data

A starting dataset composed of 46 persons with their Parent/Children and friendship information, separated in 5 different families, is available in the `data.yml` file at the root of the project.

