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

from flask import Flask, request, jsonify, session
import openai
# import os
# from dotenv import load_dotenv
import requests

# @app.route('/index', method=['GET'])
# def index():
#     return render_template('input.html')

# load_dotenv()

app = Flask(__name__)

openai.api_key = 'sk-proj-bnfWULz43QZnCRdOemrXT3BlbkFJ1wuvzmDNYlt1k7wf5vki'
# openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        # user_input = request.json.get('chat')
        # print(user_input) #remove this print later
        # if not user_input:
        #     return jsonify({'error': 'no input provided'}), 400
        # if 'messages' not in session:
        #     session['messages'] = []
        # for item in session['messages']:    #remove this print later
        #       print(item)

        # response = openai.ChatCompletion.create(
        #     engine="text-davinci-003",
        #     prompt=user_input,
        #     max_tokens=150
        # )
        # chat_response = response.choices[0].text.strip()
        # return jsonify({'response': chat_response})
        data = {
            "model": "gpt-4",
            "messages": [
                {
                    "role": "user",
                    "content": "Can you help me with something?"
                }
            ],
            "max_tokens": 150
        }
        headers = {
            'Authorization': 'Bearer sk-proj-bnfWULz43QZnCRdOemrXT3BlbkFJ1wuvzmDNYlt1k7wf5vki',
            'Content-Type': 'application/json'
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        print(response.status_code)

    

        # if response.status_code == 200:
        #             result = response.json()
        #             bot_message = result['choices'][0]['message']['content']
        #             session['messages'].append({"role": "assistant", "content": bot_message})
        #             return jsonify({'response': bot_message})
        # else:
        #             return jsonify({'error': f"Request failed with status code {response.status_code}: {response.text}"}), 500
                  
    except openai.error.OpenAIError as e:
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        return jsonify({'error': 'An error occured'}), 500


header = {
    'Authorization': 'Bearer sk-proj-bnfWULz43QZnCRdOemrXT3BlbkFJ1wuvzmDNYlt1k7wf5vki',
    # 'Authorization': f"Bearer {openai.api_key}",
    'Content-Type': 'application/json'
}


# print(response.json())

# if response.status_code == 200:
#     result = response.json()
#     print(result['choices'][0]['message']['content'])
# else:
#     print(f"Request failed with status code {response.status_code}: {response.text}")

if __name__ == '__main__':
    if not openai.api_key:
        raise ValueError('No openAI API key found. Set the OPENAI_API_KEY variable.')
    app.run(debug=True)




    """from flask import Flask, request, jsonify, session
import openai

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_input = request.json.get('chat')
        if not user_input:
            return jsonify({'error': 'No input provided'}), 400
        
        if 'messages' not in session:
            session['messages'] = []

        # Add user message to the session
        session['m
        
        
        {
  "model": "gpt-4",
  "messages": [
    {
      "role": "user",
      "content": "Can you help me with something?"
    }
  ],
  "max_tokens": 150
}
"""