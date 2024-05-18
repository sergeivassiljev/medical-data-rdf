import requests
import pandas as pd

# file read
def read_query_template(file_path='rdf_prompt_template.txt'):
    with open(file_path, 'r') as file:
        return file.read()

# Funktsioon Flask-serverile päringu saatmiseks
def send_request_to_flask(endpoint, text):
    response = requests.post(endpoint, json={'text': text})
    if response.ok:
        return response.json()
    else:
        return None

# Põhifunktsioon päringute tegemiseks ja tulemuste salvestamiseks
def perform_requests_and_save_to_excel(endpoint, text_template, num_requests=200):
    results = []

    for _ in range(num_requests):
        result = send_request_to_flask(endpoint, text_template.format(medical_text="PROMT"))
        if result is not None:
            results.append(result)

    # save into Excel
    df = pd.DataFrame(results)
    df.to_excel('request_responses_6.xlsx', index=False)

if __name__ == "__main__":
    FLASK_ENDPOINT = 'http://localhost:5000/generate_rdf'
    text_template = read_query_template()

    perform_requests_and_save_to_excel(FLASK_ENDPOINT, text_template)