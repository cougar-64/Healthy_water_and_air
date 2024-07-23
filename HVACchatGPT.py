"""The purpose of this program is to use AI to answer any HVAC related questions in a chatGPT type environment"""

from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv
import requests


load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv('OPENAI_API_KEY') or 'sk-zS5HgVGaDSftbtvZCQqaT3B1bkFJR9yGfTM3jmcIZAiTn1PM'

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('chat')
        if not user_input:
            return jsonify({'error': 'no input provided'}), 400
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        return jsonify(response.choices[0].text.strip())

    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occured'}), 500

# headers = {
#     'Authorization': 'Bearer sk-zS5HgVGaDSftbtvZCQqaT3B1bkFJR9yGfTM3jmcIZAiTn1PM',
#     'Content-Type': 'application/json'
# }
# data = {
#     "model": "gpt-4",
#     "messages": [
#         {"role": "system", "content": "You are a helpful assistant."},
#         {"role": "user", "content": "How do I make an API request to ChatGPT?"}
#     ]
# }

# response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)

# if response.status_code == 200:
#     result = response.json()
#     print(result['choices'][0]['message']['content'])
# else:
#     print(f"Request failed with status code {response.status_code}: {response.text}")

if __name__ == '__main__':
    if not openai.api_key:
        raise ValueError('No openAI API key found. Set the OPENAI_API_KEY variable.')
    app.run(debug=True)