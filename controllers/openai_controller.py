from flask import Blueprint, request, jsonify

import openai
import os
from random import choice

openai.api_key = os.environ.get("OPENAI_API_KEY")


openai_bp = Blueprint('openai', __name__, url_prefix='/openai')



@openai_bp.post('/description')
def generate_description():
    '''Generate a description of a GitHub repository using OpenAI'''

    
    repository_url = request.json.get('githubURL')
    
    # prompt = f"Give a short description of the following github repository: {repository_url}. User 20 words or less. Don't mention the github repository in the description."
    
    prompt = f"Give a detailed description of the following github repository: {repository_url}. Don't mention the github repository in the description. Explain how the code works and briefly describe the relevent web technologies used. Don't use the words 'project' or 'repository' in the description."
    
    description = ''
    
    # Query OpenAI to generate description
    try:
        description = get_openai_response(prompt)
    except Exception as err:
        print(err)
        
    # Clean up description
    description = description.replace("This is a", "A")
    
    # NOT USED
    # description = description.replace("This repository ", "")
    # description = description.capitalize()
    
    
    return jsonify(description=description), 200 # OK
    
    
    
@openai_bp.post('/image_prompt')
def generate_image_prompt():
    '''Generate an image prompt for a GitHub repository'''
    
    github_url = request.json.get('githubURL')
    
    # Query OpenAI to generate prompt
    try:
        # openai_response = get_openai_response(f"Summarize the following repository in one word: {github_url}")
        # openai_response = get_openai_response(f"In one sentence, describe the contents of a picture that represents the following github repository: {github_url}. Don't say 'The picture depicts' or 'In this picture' or make any mention of the picture itself.")
        openai_response = get_openai_response(f"In one sentence, describe an image that would make a good cover photo for the following git repository: {github_url}. Don't mention the repository in the response. ")
        
        
        suffix = choice([
            # 'pixel art',
            'digital art',
        ])

        # image_prompt = f"An abstract illustration of {openai_response}, {suffix}"

        # just get the first 10 words
        # image_prompt = ' '.join(openai_response.split()[:10]) 
        
        image_prompt = f"{openai_response}, {suffix}"
        
        return jsonify(image_prompt=image_prompt), 200 # OK
    
    except Exception as err:
        print(err)
        return jsonify(message=err), 500 # Internal Server Error



@openai_bp.post('/image')
def generate_image():
    '''Generate an image using OpenAI Dall-E'''

    image_prompt = request.json.get('imagePrompt')

    # Query OpenAI to generate image
    try:
        response = openai.Image.create(
			prompt=image_prompt,
			n=1,
			size="512x512",
			response_format="b64_json"
		)
        
        image = response.data[0]['b64_json']
        
        return jsonify(message='Image generated', image=image), 200 # OK
        
    except Exception as err:
        print(err)
        return jsonify(message=err), 500 # Internal Server Error
    


def get_openai_response(prompt):
    '''Query the OpenAI text-completion language model using a input prompt'''

    # response = openai.Completion.create(
    #     model='text-davinci-003',
    #     prompt=prompt,
    #     temperature=0.6,
    #     max_tokens=1024
    # )
    
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                'role': 'user', 
                'content': prompt
            }
        ]
    )
    
    
    result = response['choices'][0]['message']['content']
    #  or result = response.choices[0].message.content
    
    # OLD WAY using text-davinci-003 model
    # return response.choices[0].text.strip()
    
    return result
    
    


# @openai_bp.post('/tags')
# def generate_tags():
#     print(request.json)
#     description = 'hello'
    
#     repository_url = request.json['githubURL']
    
#     prompt = f'What are the primary web technologies used by the following github repository: #{repository_url}'
    
#     response = openai.Completion.create(
# 		model='text-davinci-003',
# 		prompt=prompt,
# 		temperature=0.6,
# 		max_tokens=1024
# 	)
    
#     description = response.choices[0].text
    
#     return jsonify(description=description), 200