from flask import Flask, render_template, url_for, request
import requests
from openai import OpenAI
import json

app = Flask(__name__)
API_KEY = open("API_KEY", 'r').read()

client = OpenAI(
    # This is the default and can be omitted
    api_key=API_KEY,
)

@app.route('/')
def index():
    story = """
    One rainy night Maya was walking home early, when she saw a dog shivering with cold in a corner. Seeing his wet hair and scared face, he felt pity.
    Maya slowly went to that dog and covered it with her umbrella. At first the dog was a little scared, but feeling the kindness of Maya, moved forward a little and came under the umbrella. His trembling body slowly calmed down.
    Maya and the dog started walking towards the house together. Maya started feeling a deep relief. He realized that the happiness of the one who does kindness is not only given to the troubled person, but also to the person who helps.
    Without thinking twice, Maya decided that she would adopt the dog and take care of it with love and give it a new life. The dog, now named Lucky, started living with Maya at her house.
    This heartwarming story reminds us how small acts of kindness can make a big difference. It makes us understand that, we should take care of the sorrows and sufferings around us and should always extend a helping hand whenever possible. We can make a deep impact in the world with our kindness.
    """
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
    return render_template('index.html', data="Hello")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)