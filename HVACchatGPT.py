"""The purpose of this program is to use AI to answer any HVAC related questions in a chatGPT type environment"""

"""notes:
- no image uplaoding allowed
- maybe it can prompt the user with a couple of questions (explain how an HVAC system works, should I change my filter, etc.)
- create a database for:
    - keeping track of what was most searched in a given time period (using keywords 'LIKE' to return unique yet similar requests)
    - if they found the response helpful
    - timestamp of the search
    - geographical location of search?
    - weather at time of search
    we can then make specific videos based on what questions were most searched
- train the bot to recommend our company for fixes
- store single chat history in a list to keep context for the bot
"""

from flask import Flask, request, jsonify
import openai
# import os
# from dotenv import load_dotenv
import requests


# load_dotenv()

app = Flask(__name__)

openai.api_key = 'sk-proj-bnfWULz43QZnCRdOemrXT3BlbkFJ1wuvzmDNYlt1k7wf5vki'
# openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('chat')
        if not user_input:
            return jsonify({'error': 'no input provided'}), 400
        response = openai.ChatCompletion.create(
            engine="text-davinci-003",
            prompt=user_input,
            max_tokens=150
        )
        header = {
            'Authorization': 'Bearer sk-proj-bnfWULz43QZnCRdOemrXT3BlbkFJ1wuvzmDNYlt1k7wf5vki',
            # 'Authorization': f"Bearer {openai.api_key}",
            'Content-Type': 'application/json'
        }
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ]
        }

        response = requests.post('https://api.openai.com/v1/chat/completions', headers=header, json=data)
        if response.status_code == 200:
            result = response.json()
            print(result['choices'][0]['message']['content'])
        else:
            result = "idk"
            print(result)
            # print(f"Request failed with status code {response.status_code}: {response.text}")
        # print(response.json())
        chat_response = response.choices[0].text.strip()
        return jsonify({'response': chat_response})
    

    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occured'}), 500


if __name__ == '__main__':
    if not openai.api_key:
        raise ValueError('No openAI API key found. Set the OPENAI_API_KEY variable.')
    
    app.run(debug=True, use_reloader=False)



'''issues:
- Server isn't waiting for UI to send me anything (line 64,65)
- Need to send back to front end so it can print it'''