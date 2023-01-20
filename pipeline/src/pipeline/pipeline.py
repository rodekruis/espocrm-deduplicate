from pipeline.espo_api_client import EspoAPI, EspoAPIError
import os
from fuzzywuzzy import fuzz
import pandas as pd
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
    #define dataframe for dedupe
    df = pd.DataFrame(columns=['Entity1', 'field1', 'Entity2','field2'])
    
    #fill dataframe with entities you want to check (user input)
    df.loc[1] = ['ent1', 'f1', 'ent2', 'f2']
    df.loc[2] = ['entA', 'fA', 'entA', 'fA']

    #check for duplicates in each field-pair defined in the dataframe
    for x in range(len(df)):
        x=x+1
        entity_name_1 = df['Entity1'][x]
        duplicated_field_1 = df['field1'][x]
        entity_name_2 = df['Entity2'][x]
        duplicated_field_2 = df['field2'][x]

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
                    try:
                        espo_client.request('PUT', f'{entity_name_2}/{entity_2["id"]}', {'isDuplicate': True})
                    except:
                        #first create isDuplicate field
                        data = {
                            "type": "bool",
                            "name": "isDuplicate",
                            "label": "isDuplicate",
                            "default": False,
                            "audited": False,
                            "readOnly": True
                        }
                        espo_client.request('POST', f'Admin/fieldManager/{entity_name_2}', data)
                        espo_client.request('PUT', f'{entity_name_2}/{entity_2["id"]}', {'isDuplicate': True})