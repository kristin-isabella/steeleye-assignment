import json
import logging

# Configure the logger
from lambda_handler import lambda_handler

logging.basicConfig(level=logging.INFO)


def run(url: str):
    # Define input parameters for the lambda_handler function
    event = {'url': url}
    # Define the file type to download
    event = json.dumps(event)
    # Call the lambda_handler function
    response = lambda_handler(event=event, context=None)


if __name__ == "__main__":
    run(url="https://registers.esma.europa.eu/solr/esma_registers_firds_files/"
            "select?q=*&fq=publication_date:%5B2021-01-17T00:00:00Z+TO+2021-01-19T23:59:59Z%5D&wt=xml&"
            "indent=true&start=0&rows=100"
        )