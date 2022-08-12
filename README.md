# espocrm-deduplicate

Dockerized app to deduplicate entries in EspoCRM.

Developed in support to the [Ukraine crisis 2022](https://go.ifrc.org/emergencies/5854).

## Description

Synopsis: a [dockerized](https://www.docker.com/) [python app](https://www.python.org/) that checks for duplicated entries in [EspoCRM](https://www.espocrm.com/).

Worflow: the app periodically checks if field X in entity A equals field Y in entity B. If so, set a defined boolean field as true.
Repeat for all entities A and B. Supports fuzzy matching.

## Setup

Add EspoCRM API keys and URL in `credentials/.env`.

Deploy with [Azure Logic Apps](https://azure.microsoft.com/en-us/services/logic-apps/#overview) as per [instructions](https://docs.google.com/document/d/182aQPVRZkXifHDNjmE66tj5L1l4IvAt99rxBzpmISPU/edit?usp=sharing).
