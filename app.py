from flask import Flask, Response, render_template, url_for, request, jsonify
import requests
from openai import OpenAI
import json
import time

app = Flask(__name__)
API_KEY = open("API_KEY", 'r').read()

client = OpenAI(
    # This is the default and can be omitted
    api_key=API_KEY,
)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the input value from the form
        input_value = request.form['input_value']

        # Define a function to generate story chunks
        def generate_story_chunks():
            # Formulate the query
            query = [{
                "role": "user",
                "content": "Write a short story based on the topic: " + input_value + " The story should be four or five paragraph long."
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
        
    return render_template('index.html')


@app.route('/generate_comic', methods=['GET','POST'])
def generate_comic():
    data = request.json['content']
    print(data)

    response = client.images.generate(
        model="dall-e-2",
        prompt= "Story: " + data + "This is a short story. Generate a colorful comic like image based on the story given.",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    
    print(image_url)
    return image_url
    # if request.is_json:
    #     content = request.json['content']
    #     print(content)  # Do something with the content
    #     return render_template('generate_comic.html', data = content)
    # else:
    #     return jsonify({'error': 'Unsupported Media Type'}), 415
    
    # if request.method == 'POST':
    #     pass
    # else:
    #     return render_template('generate_comic.html', data = "No content received")
# @app.route('/generate_story', methods = ['GET','POST'])
# def generate_story():
#     return render_template('generate_story.html', data="Hello") 

# def generate_story_chunks(input_value):
#     print(input_value)
#     query = [{
#         "role": "user",
#         "content": "Write me a short story about " + input_value
#     }]

#     chat_completion_response = client.chat.completions.create(
#         messages=query,
#         model="gpt-3.5-turbo",
#         stream=True
#     )

#     for chunk in chat_completion_response:
#         if chunk.choices[0].delta.content is not None:
#             yield chunk.choices[0].delta.content.strip() + ' '
#         else:
#             yield ''  # Yield an empty chunk if no content is available
#         # time.sleep(1)  # Simulate processing delay

# @app.route('/generate_story/create', methods= ['GET','POST'])
# def create_story():

#     if request.method == "POST":
#         story_topic = request.form['input_value']
#         print(story_topic)
#         return Response(generate_story_chunks(story_topic), mimetype='text/html')
    
#     return render_template('story.html', data="Hello")


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)