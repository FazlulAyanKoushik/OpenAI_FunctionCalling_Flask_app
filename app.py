from flask import Flask, request, jsonify, session
from openai import OpenAI
from decouple import config
import json
from flask_session import Session
from instruction import instructions

from datetime import timedelta
from helpers import (
    get_available_foods,
    create_order,
    update_order,
    available_functions,
    functions
)

openAI_key = config('OPENAI_KEY')

client = OpenAI(api_key=openAI_key)

app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/chat',)
def index():
    user_message = request.json.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    # Initialize or fetch conversation history for the session
    if 'messages' not in session:
        session['messages'] = [{
            "role": "system",
            "content": instructions
        }]

    # Add the user's message to the conversation
    session['messages'].append({"role": "user", "content": user_message})

    # Call the OpenAI API with current conversation
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=session['messages'],
        functions=functions,
        function_call="auto"
    )

    response_message = response.choices[0].message
    response_content = response.choices[0].message.content

    # store chatbot response message to session message tread
    session['messages'].append(response_message)

    try:
        function_name = response.choices[0].message.function_call.name
        function_args = json.loads(response.choices[0].message.function_call.arguments)
    except:
        function_name = None
        function_args = {}

    # Handle function call if necessary
    if function_name:
        if function_args is not {}:
            function_message = available_functions[function_name](**function_args)
        else:
            function_message = available_functions[function_name]()

        session['messages'].append(
            {
                "role": "function",
                "name": function_name,
                "content": function_message
             }
        )

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=session['messages'],
        )

        response_message = response.choices[0].message
        response_content = response.choices[0].message.content
        session['messages'].append(response_message)

    return jsonify(
        {"message": response_content}
    ), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
