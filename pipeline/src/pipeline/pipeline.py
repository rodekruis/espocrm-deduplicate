from pipeline.espo_api_client import EspoAPI, EspoAPIError
import os
from fuzzywuzzy import fuzz
from dotenv import load_dotenv
import logging
logging.root.handlers = []
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.DEBUG, filename='ex.log')
# set up logging to console
console = logging.StreamHandler()
console.setLevel(logging.WARNING)
# set a format which is simpler for console use
formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(message)s')
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)
twilio_logger = logging.getLogger('twilio.http_client')
twilio_logger.setLevel(logging.WARNING)
load_dotenv(dotenv_path="../credentials/.env")

# create a client to EspoCRM
espo_client = EspoAPI(os.getenv("ESPO_URL"), os.getenv("ESPO_KEY"))


def main():
    # define entities and fields to check
    entity_name_1 = "bumfuzzle"
    duplicated_field_1 = "name"
    entity_name_2 = "cattywampus"
    duplicated_field_2 = "name"

    # get all entities from EspoCRM
    entities_1 = espo_client.request('GET', entity_name_1)['list']
    entities_2 = espo_client.request('GET', entity_name_2)['list']

    # loop over entities
    for entity_1 in entities_1:
        # check if field in entity, else raise error
        if duplicated_field_1 not in entity_1:
            logging.error(f"{duplicated_field_1} not in {entity_1}!")
            continue
        for entity_2 in entities_2:
            # check if field in entity, else raise error
            if duplicated_field_2 not in entity_2:
                logging.error(f"{duplicated_field_2} not in {entity_2}!")
                continue

            # check if fields are duplicated
            is_duplicate = entity_1[duplicated_field_1] == entity_2[duplicated_field_2]
            if fuzz.ratio(entity_1[duplicated_field_1], entity_2[duplicated_field_2]) > 0.95:
                is_duplicate = True

            # update duplication field
            if is_duplicate:
                espo_client.request('PUT', f'Case/{entity_2["id"]}', {'isDuplicate': is_duplicate})