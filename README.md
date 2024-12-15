# ba-biler

## Overview

This README provides the necessary information to set up, configure, and use the microservice. It includes details about environmental variables, API endpoints, and dependencies.

The service can be accesed here: https://ba-biler-hagae6gdgacvafaf.northeurope-01.azurewebsites.net/apidocs


---

## Environmental Variables

The microservice requires the following environmental variables to be configured before running. Ensure these variables are set correctly in your environment.

| Variable  | Required | Default | Description                |
| --------- | -------- | ------- | -------------------------- |
| `DB_PATH` | Yes      | None    | Path to the database file. |

---

## API Endpoints

Below is a list of the API endpoints exposed by this microservice. Each endpoint includes the HTTP method, a brief description, possible status codes, and the returned data.

### Endpoints

| Path                  | Method | Description                      | Status Codes   | Response                                                |
|-----------------------|--------|----------------------------------|----------------|---------------------------------------------------------|
| `/biler`              | GET    | Get all cars                     | 200, 404, 500  | Array of objects with `nummerplade`, `maerke`, and `abonnement_pris`. |
| `/biler/udlejet`      | GET    | Get all rented cars              | 200, 404, 500  | Array of objects with `nummerplade`, `maerke`, and `abonnement_pris`. |
| `/biler/udlejet/total`| GET    | Get total price for udlejet      | 200, 404, 500  | Object with `total` as an integer.                     |
| `/biler/<nummerplade>`| PATCH  | Update rental status of a car    | 200, 400, 404, 500 | Object with `message` indicating success or error.      |

---

## Dependencies

The following dependencies are required to run the microservice. These are specified in the `requirements.txt` file:

---
