from flask import Flask, Response, render_template, url_for, request, jsonify
import requests
from openai import OpenAI
import json
import time

app = Flask(__name__)
API_KEY = open("API_KEY", 'r').read()

client = OpenAI(api_key=API_KEY)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('landing.html')
    

@app.route('/generate/story/comic', methods=['GET','POST'])
def generate_comic():
    data = request.json['content']
    len(data)

    response = client.images.generate(
        model="dall-e-3",
        prompt= "Story: " + data + "This is a short story. Generate a colorful comic like image without any text based on the story given.",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    image_url = response.data[0].url
    return image_url

@app.route('/generate/story', methods=['GET', 'POST'])
def gen_story():
    if request.method == 'POST':
        # Get the input value from the form
        input_value = request.form['input_value']

        # Define a function to generate story chunks
        def generate_story_chunks():
            # Formulate the query
            query = [{
                "role": "user",
                "content": "Write a ten paragraph story based on the topic: " + input_value
            }]

            # Make a request to GPT API with stream=True
            chat_completion_response = client.chat.completions.create(
                messages=query,
                model="gpt-3.5-turbo",
                stream=True
            )

            # Yield each chunk of the response
            for chunk in chat_completion_response:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content + ''
                else:
                    yield ''  # Yield an empty chunk if no content is available

        # Return a response with the generator function as content
        return Response(generate_story_chunks(), mimetype='text/plain')
        
    return render_template('generate_story.html')



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)