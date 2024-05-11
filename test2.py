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
def perform_requests_and_save_to_excel(endpoint, text_template, num_requests=100):
    results = []

    for _ in range(num_requests):
        result = send_request_to_flask(endpoint, text_template.format(medical_text="Abdominal and pelvic region Clinical data: Fell while sledding. FINDINGS: The pancreas is of normal size with age-appropriate structure, no volumetric changes observed. The liver is of normal size with a uniform structure, no focal lesions detected. Gallbladder walls are thin, lumen is clear. Bile ducts are not dilated. The spleen is not enlarged, no focal lesions found. Kidneys' size, position, and structure are normal. No swelling in the kidneys. The bladder is minimally filled, contents are echo-free. The abdominal aorta and iliac vessels in the visible section are of normal diameter, blood flow is normal. No enlarged lymph nodes seen retroperitoneally. No free fluid detected in the abdominal cavity."))
        if result is not None:
            results.append(result)

    # save into Excel
    df = pd.DataFrame(results)
    df.to_excel('request_responses4.xlsx', index=False)

if __name__ == "__main__":
    FLASK_ENDPOINT = 'http://localhost:5000/generate_rdf'
    text_template = read_query_template()

    perform_requests_and_save_to_excel(FLASK_ENDPOINT, text_template)