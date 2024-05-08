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
    
@app.route('/generate/summary', methods=['GET', 'POST'])
def generate_summary():
    return render_template('generate_summary.html')

@app.route('/generate/summary/show', methods=['GET', 'POST'])
def generate_summary_show():
    if request.method == 'POST':
        # Get the input value from the form
        comic_input = request.form['comic_input']
        query = [{
            "role": "user",
            "content": "Your task is to summarise stories. Here is a short story for you. Summarise it with 5 bullet points and return the points in a json object. Here is the story: " + comic_input 
            + """ \n The format of return should be a JSON object
            
            {
                "summary": [line 1, line 2, line 3]
            }
            
            """
        }]

        chat_completion_response = client.chat.completions.create(
            messages=query,
            model="gpt-3.5-turbo"
        )
        summary = chat_completion_response.choices[0].message.content.strip('\n').strip()
        summary_dict = json.loads(summary)
        summary_lst = summary_dict['summary']

        comic_images = []
        for item in summary_lst:
            response = client.images.generate(
                model="dall-e-3",
                prompt= "Story Summary: " + item + "This is a single line of a story. Generate a colorful comic like image without any text based on the line given.",
                size="1024x1024",
                quality="standard",
                n=1,
            )
            imgurl = response.data[0].url
            comic_images.append(imgurl)

        summary_comic = {}
        for i in range(len(summary_lst)):
            summary_comic[i] = [summary_lst[i],comic_images[i]]
        
        print(summary_comic)
        return render_template('show_comic.html', data = summary_comic)
    return render_template('generate_summary.html')

    
@app.route('/generate/story/comic', methods=['GET','POST'])
def generate_comic():
    data = request.json['content']
    
    # generate_summary(data)

    response = client.images.generate(
        model="dall-e-3",
        prompt= "You are a comic artist. Here is a short story for you: " + data + "Generate a colorful comic like image without any text based on the story given.",
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