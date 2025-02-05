# Technical Challenge - Software Engineer - Backend

## Goal

The goal of this challenge is to build the prototype of an API for a social network that will be able to manage any number of People and capture different types of relationships between them

For each People the system will record 3 informations
- First name
- Last name
- Nickname (Optional)

Between 2 People the system will be able to capture two types of relationships
- Friendship information (a friendship will automatically be bi-directional)
- Family information (parent, kid)

In additional to the CRUD endpoints required to manage People and their relationships, the system should expose 2 API to query information
- Query all ancestors for a given person
- Query all family’s friends of any given person. (family’s friend is defined as someone who’s friend with any member of your family)

> The final solution must include at least one unit test.

## Technical Stack

- FastAPI must be used for the web server
- Neo4j must be used for the database
- The standard Neo4j library must be used to interact with the database (no OGM) https://neo4j.com/docs/api/python-driver/current/

## Resource Available

A docker compose is provided to start a local docker container, otherwise it's possible to use a free Cloud instance of Neo4j in the Cloud https://neo4j.com/cloud/platform/aura-graph-database/
Gitpod can be used to spin up a development environment if needed

## Data

A starting dataset composed of 46 persons with their Parent/Children information, separated in 5 different families, is available in the `data.yml` file at the root of the project.

> The friendship information are not represented in this dataset, it’s up to you to generate them

> This dataset is mainly here to help you get started and it can be modified as you see fit.

## Share your code

Once completed, please commit your code to this repository and send us an email at `tech-challenge-support@opsmill.com` so we can have a look and decide the next steps in the interview process.

> Please don't upload your code in a public Git repository

## Contact / Support

Please email your questions to `tech-challenge-support@opsmill.com`