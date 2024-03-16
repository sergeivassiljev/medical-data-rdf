from flask import Flask, request, jsonify
import openai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Замените на ваш API ключ от OpenAI
openai.api_key = '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'

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
        return f"Ошибка при генерации текста: {str(e)}"



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
    prompt = f"Convert the following medical description to RDF format and divide by N numbers (make it more structured): \"{text}\".\n\nExpected RDF format:\n<subject> <predicate> <object>\n"

    response = openai.completions.create(
          model="gpt-3.5-turbo-instruct",
          prompt=prompt,
          temperature=0.7,
          max_tokens=2000,
          top_p=1.0,
          frequency_penalty=0.0,
          presence_penalty=0.0
        )
    generated_text = response.choices[0].text.strip()

    translated_text = translate_text_with_gpt(generated_text)

    return jsonify({"generated_rdf": generated_text, "translated_rdf": translated_text})



if __name__ == '__main__':
    app.run(debug=True)




if __name__ == '__main__':
    app.run(debug=True)



# openai.api_key = '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'