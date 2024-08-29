## invoice extractor 

# comment out for streamlit cloud run. 
#from dotenv import load_dotenv 

#load_dotenv() 
#%pip install google-generativeai
#%pip install streamlit

import streamlit as st 
import os 
from PIL import Image 
import google.generativeai as genai 

## configure api key 

genai.configure(api_key = os.getenv("GOOGLE_API_KEY"))

## function to load gemini pro vision model and get response 

def get_gemini_response(input, image, prompt): 
    ## loading the model 
    
    # from streamlit cloud: 
    #NotFound: 404 Gemini 1.0 Pro Vision has been deprecated on July 12, 2024. 
    #Consider switching to different model, for example gemini-1.5-flash.
    #model = genai.GenerativeModel('gemini-pro-vision')
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input, image[0], prompt])
    return response.text 

def input_image_setup(uploaded_file): 
    if uploaded_file is not None: 
        # read the file into bytes 
        bytes_data = uploaded_file.getvalue() 

        image_parts = [ {"mime_type": uploaded_file.type, "data": bytes_data}]

        return image_parts 
    else: 
            raise FileNotFoundError("No file uploaded")


##  initialize streamlit app 

st.set_page_config(page_title="Gemini Image Recognition")

st.header("Gemini Image REcognition")

uploaded_file = st.file_uploader("Choose an image ... ", type=["jpg", "jpeg", "png"])
input=st.text_input("Input Prompt: ", key="input")

image="" 

if uploaded_file is not None: 
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit = st.button("Tell me about the image")

input_prompt = """
You are an expert in recognizing objects in an image. 
You will receive input image and answer questions based on this image. 
""" 

if submit: 
     image_data = input_image_setup(uploaded_file)
     response = get_gemini_response(input_prompt, image_data, input)

     st.subheader("The response is")
     st.write(response)

     

