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
    - Needs to be saved for a certain amount of time? 
- make the AI print out as it's typing, not just wait for a long time until it prints in a big block
"""

from flask import Flask, request, jsonify, session as flask_session
import openai
import os
from dotenv import load_dotenv
import logging
import time
from flask_cors import CORS
from flask_session import Session
import traceback


load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'  # Ensure this directory exists
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 86400
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'session:'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'test_session_1'  # Set a custom session cookie name
Session(app)

# logging to console
logging.basicConfig(level=logging.DEBUG)

@app.before_request
def before_request():
    app.logger.info(f"Session ID: {app.config['SESSION_COOKIE_NAME']}")
    app.logger.info(f"Session Data Before: {dict(flask_session)}")


@app.route('/chat', methods=['POST'])
def chat():
    app.logger.info("endpoint /chat was hit")
    try:
        app.logger.info("Request method: %s", request.method)
        app.logger.info("Request data: %s", request.data.decode('utf-8'))
        user_input = request.json.get('chat')
        if not user_input:
            return jsonify({'error': 'no input provided'}), 400
        
         # Initialize the conversation history if it doesn't exist
        if 'conversation' not in flask_session:
            app.logger.info("Initializing conversation history in session")
            flask_session['conversation'] = []

            app.logger.info(f"Current conversation history before update: {flask_session['conversation']}")


        # Add the user's input to the conversation history
        flask_session['conversation'].append({"role": "user", "content": user_input})
        
        start_time = time.time()
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=flask_session['conversation'],
            max_tokens=150
        )
        end_time = time.time()
        app.logger.info("OpenAI response time: %s seconds", end_time - start_time)

        reply = response['choices'][0]['message']['content'].strip()
        app.logger.info("OpenAI response: %s", reply)
        flask_session['conversation'].append({"role": "assistant", "content": reply})      
        app.logger.info(f"Updated conversation history: {flask_session['conversation']}")      
        flask_session.modified = True
    
        return jsonify({'response': reply, 'conversation': flask_session['conversation']})
    

    except openai.ErrorObject as e:
        app.logger.error('Authentication error: %s', e)
        return jsonify({'error': 'Authentication error: ' + str(e)}), 401
    except openai.OpenAIError as e:
        app.logger.error('OpenAI API error: %s', e)
        return jsonify({'error': 'OpenAI API error: ' + str(e)}), 500
    except Exception as e:
        app.logger.error('An error occurred: %s', e)
        app.logger.error(traceback.format_exc())
        return jsonify({'error': 'An error occurred: ' + str(e)}), 500
    


if __name__ == '__main__':
    if not openai.api_key:
        raise ValueError('No openAI API key found. Set the OPENAI_API_KEY variable.')
    
    app.run(debug=True, use_reloader=False) #write a try except condition to catch when the address is already in use

'''issues:
    - conversation history isn't being saved after each request
    - conversation history is empty at beginning of each request
    - I think it's a front end issue with the `sendMessage` function 8/1/24 1:47pm'''

