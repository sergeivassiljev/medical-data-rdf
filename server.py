from flask import Flask, request, jsonify
import openai
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)



openai.api_key = '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'

def create_db_and_table():
    conn = sqlite3.connect('requests_responses.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS requests_responses
                 (id INTEGER PRIMARY KEY, response_text TEXT, timestamp TEXT)'''),
    conn.commit()
    conn.close()

create_db_and_table()

def add_request_response_to_db(response_text):
    conn = sqlite3.connect('requests_responses.db')
    c = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO requests_responses (response_text, timestamp) VALUES (?, ?)",
              (response_text, current_time))
    conn.commit()
    conn.close()

def generate_with_gpt3(prompt):
    try:
        response = openai.completions.create(
          model="gpt-3.5-turbo-instruct",
          prompt=prompt,
          temperature=0.7,
          max_tokens=300,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error while generating: {str(e)}"

@app.route('/process-text', methods=['POST'])
def process_text():
    data = request.get_json()
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt = f"Please correct the medical text for punctuation, grammar, and typographical errors: '{data['text']}'",
        max_tokens=3000
    )
    corrected_text = response.choices[0].text.strip()
    return jsonify({'correctedText': corrected_text})

def translate_text_with_gpt(text, source_language='English', target_language='Estonian'):
    response = openai.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=f"Translate the following text from {source_language} to {target_language}:\n\n{text}",
        temperature=0.3,
        max_tokens=1024
    )
    return response.choices[0].text.strip()

@app.route('/generate_rdf', methods=['POST'])
def generate_rdf():
    data = request.json
    text = data.get('text', '')
    
    # Malli lugemine failist
    with open('rdf_prompt_template.txt', 'r') as file:
        prompt_template = file.read()
    
    # Teksti lisamine malli
    prompt = prompt_template.format(medical_text=text)
    
    response = openai.completions.create(
          model="gpt-3.5-turbo-instruct",
          prompt=prompt,
          temperature=0.6,
          max_tokens=3000,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
    
    generated_text = response.choices[0].text.strip()
    add_request_response_to_db(generated_text)


    return jsonify({"generated_rdf": generated_text})

@app.route('/generate_medical_report', methods=['POST'])
def generate_medical_report():
    data = request.json
    rdf_data = data.get('rdf_data', '')
    
    # RDF teksti põhjal päringu koostamine
    prompt = f"Tehke meditsiiniline järeldus järgmiste andmete põhjal aruande kujul ja kirjutage, millele tuleks erilist tähelepanu pöörata: {rdf_data} "
    
    response = openai.completions.create(
          model="gpt-3.5-turbo-instruct",
          prompt=prompt,
          temperature=0.6,
          max_tokens=2000,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
    
    generated_report = response.choices[0].text.strip()
    add_request_response_to_db(generated_report)  # Функция для сохранения в БД

    return jsonify({"generated_report": generated_report})

# @app.route('/generate_rdf', methods=['POST'])
# def generate_rdf():
#     data = request.json
#     text = data.get('text', '')
    
#     # Чтение шаблона из файла для первого запроса
#     with open('rdf_prompt_template.txt', 'r') as file:
#         prompt_template = file.read()
    
#     # Формирование промпта для первого запроса
#     first_prompt = prompt_template.format(medical_text=text)
    
#     # Первый запрос к GPT-3
#     first_response = openai.completions.create(
#         model="gpt-3.5-turbo-instruct",
#         prompt=first_prompt,
#         temperature=0.3,
#         max_tokens=3000,
#         top_p=1.0,
#         frequency_penalty=0.0,
#         presence_penalty=0.0
#     )
    
#     generated_text = first_response.choices[0].text.strip()
    
#     # Формирование промпта для второго запроса, используя generated_text
#     second_prompt = "Please review the provided RDF medical text for any duplicates and inaccuracies. Correct them as needed and provide a concise response containing only the corrected text: \n\n" + generated_text
    
#     # Второй запрос к GPT-3
#     second_response = openai.completions.create(
#         model="gpt-3.5-turbo-instruct",
#         prompt=second_prompt,
#         temperature=0.7,
#         max_tokens=1000,
#         top_p=0.5,
#         frequency_penalty=0.0,
#         presence_penalty=0.0
#     )
    
#     final_text = second_response.choices[0].text.strip()
    
#     # Запись в базу данных, если необходимо
#     add_request_response_to_db(final_text)

#     return jsonify({"generated_rdf": final_text})

# if __name__ == '__main__':
#     app.run(debug=True)




if __name__ == '__main__':
    app.run(debug=True)



# openai.api_key = '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'