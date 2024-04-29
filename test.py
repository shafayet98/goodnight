# if request.method == "GET":
    #     print("Here")

    # if request.method == "POST":
    #     print("Here in POST")
    #     data = request.json or request.get_json()
    #     # id of the provided option
    #     clicked_div_id = data.get('div_id')
    #     if clicked_div_id == 'id_gen_story':
    #         print("Generating Story")
    # print(request)
    
    # story = """
    # One rainy night Maya was walking home early, when she saw a dog shivering with cold in a corner. Seeing his wet hair and scared face, he felt pity.
    # Maya slowly went to that dog and covered it with her umbrella. At first the dog was a little scared, but feeling the kindness of Maya, moved forward a little and came under the umbrella. His trembling body slowly calmed down.
    # Maya and the dog started walking towards the house together. Maya started feeling a deep relief. He realized that the happiness of the one who does kindness is not only given to the troubled person, but also to the person who helps.
    # Without thinking twice, Maya decided that she would adopt the dog and take care of it with love and give it a new life. The dog, now named Lucky, started living with Maya at her house.
    # This heartwarming story reminds us how small acts of kindness can make a big difference. It makes us understand that, we should take care of the sorrows and sufferings around us and should always extend a helping hand whenever possible. We can make a deep impact in the world with our kindness.
    # """
    # query = [{
    #     "role": "user",
    #     "content": "Here is a short story: " + story + "Here is a story. Create a short version of this story in 5 lines. It must be 5 lines. Make the response a JSON object with 'short version' as a key and your response as value.  "
    # }]
    # chat_completion_response = client.chat.completions.create(
    #                 messages=query,
    #                 model="gpt-3.5-turbo",
    # )
    # response_data = chat_completion_response.choices[0].message.content.strip('\n').strip()
    # response_json = json.loads(response_data)
    # lines = response_json['short version'].split('.')
    # lines = [line.strip() for line in lines if line.strip()]
    # print(lines)
    # print(len(lines))

    # img_urls = []
    # for itm in lines:
    #     response = client.images.generate(
    #         model="dall-e-2",
    #         prompt= itm + "This is a line from a story book. Generate an image based on the line given. Generate the image as colorful sketch form like a kid's story book.",
    #         size="256x256",
    #         quality="standard",
    #         n=1,
    #     )
    #     image_url = response.data[0].url
    #     img_urls.append(image_url)
    
    # print(img_urls)
    # print(type(img_urls))

# from flask import Flask, Response, render_template, url_for, request, jsonify
# import requests
# from openai import OpenAI
# import json
# import time

# app = Flask(__name__)
# API_KEY = open("API_KEY", 'r').read()

# client = OpenAI(
#     # This is the default and can be omitted
#     api_key=API_KEY,
# )

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     return render_template('index.html', data="Hello")

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

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port=8080)






# HTML
# <!DOCTYPE html>
# <html lang="en">

# <head>
#   <meta charset="UTF-8">
#   <meta name="viewport" content="width=device-width, initial-scale=1.0">
#   <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
#   <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet"
#     integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
#   {% block head %} {% endblock %}
# </head>

# <body>

#   <div class="container">

#     {% block body %}

#     {% endblock %}
#     <div id="prompt" class="d-flex justify-content-center mt-5">
#       <div class="mb-3 prompt">
#         <form id="generate_story_form" action="/" method="post">
#           <!-- <label for="input_value">Input Value:</label> -->
#           <textarea type="text" class="form-control main_prompt_area shadow-none" id="input_value" name="input_value"
#             placeholder="Write me a story about...(ex. ghosts, a lost cat, etc.)" rows="1" required></textarea>
#           <center>
#             <button id="button" class="mt-3" type="submit">Submit</button>
#           </center>
#         </form>
#       </div>
#     </div>


#     <div id= "comic_request" class="d-none justify-content-center mt-5">
#       <form id = "generate_comic_form" action="/generate_comic" method="post">
#         <button id="button_comic" class="mt-3" type="submit">Generate Comic</button>
#       </form>
#     </div>
    
#     <div>
#       <img id="gen_img" src="" alt="">
#     </div>

#   </div>



#   <script>
#     const storyContent = document.getElementById('story_content');
#     const form_create_story = document.querySelector('#generate_story_form');
#     const form_create_comic = document.querySelector('#generate_comic_form');
#     const prompt = document.getElementById("prompt");
#     const comic_rqst_div = document.getElementById("comic_request");


#     form_create_story.addEventListener('submit', async (e) => {
#       e.preventDefault();

#       const input_value = document.getElementById('input_value').value;
#       prompt.classList.remove('d-flex');
#       prompt.classList.add('d-none');

#       const response = await fetch('/', {
#         method: 'POST',
#         headers: {
#           'Content-Type': 'application/x-www-form-urlencoded',
#         },
#         body: `input_value=${encodeURIComponent(input_value)}`
        
#       });
#       console.log(typeof(`input_value=${encodeURIComponent(input_value)}`));
#       const reader = response.body.getReader();
#       console.log(reader);
#       let decoder = new TextDecoder();
#       let partialChunk = '';
#       while (true) {
#         const { done, value } = await reader.read();
#         if (done) {
#           comic_rqst_div.classList.remove("d-none");
#           comic_rqst_div.classList.add("d-flex");
#           break;
#         }
#         const chunk = decoder.decode(value, { stream: true });
#         partialChunk += chunk;
#         storyContent.innerHTML = partialChunk;
#       }
#     });

#     form_create_comic.addEventListener('submit', async(e) =>{
#       e.preventDefault();
#       generated_story = storyContent.innerHTML;

#       // const response = await fetch('/generate_comic', {
#       //   method: 'POST',
#       //   headers: {
#       //     'Content-Type': 'application/x-www-form-urlencoded',
#       //   },
#       //   body: `input_value=${encodeURIComponent(generated_story)}`
        
#       // });
    
#       // Send the content to the Flask app using AJAX
#       var xhr = new XMLHttpRequest();
#         xhr.open('POST', '/generate_comic', true);
#         xhr.setRequestHeader('Content-Type', 'application/json');
#         xhr.onreadystatechange = function() {
#             if (xhr.readyState === XMLHttpRequest.DONE  && xhr.status === 200) {
#                 // Handle the response from the Flask app if needed
#                 console.log(xhr.responseText);
#                 let img_url = xhr.responseText
#                 document.getElementById("gen_img").src= img_url;
#                 // window.location.href = '/generate_comic';
#             }
#         };
#         xhr.send(JSON.stringify({ content: generated_story }));

#     })

#   </script>
# </body>

# </html>




# API STREAM
# def generate_story_chunks():
#             # Formulate the query
#     query = [{
#         "role": "user",
#         "content": "Write a short story based on the topic: " + input_value + " The story should be four or five paragraph long."
#     }]

#     # Make a request to GPT API with stream=True
#     chat_completion_response = client.chat.completions.create(
#         messages=query,
#         model="gpt-3.5-turbo",
#         stream=True
#     )

#     # Yield each chunk of the response
#     for chunk in chat_completion_response:
#         if chunk.choices[0].delta.content is not None:
#             yield chunk.choices[0].delta.content + ''
#         else:
#             yield ''  # Yield an empty chunk if no content is available

# # Return a response with the generator function as content
# return Response(generate_story_chunks(), mimetype='text/plain')