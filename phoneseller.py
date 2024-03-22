import json
import openai
import csv
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = "https://ai-proxy.lab.epam.com"



def cargar_datos(archivo):
    datos = []
    with open(archivo, newline='', encoding='utf-8') as csvfile:
        lector = csv.DictReader(csvfile)
        for fila in lector:
            datos.append(fila)
    return datos

dataset = cargar_datos('datos_telefonos.csv')
data = json.dumps(dataset)

prompt = """ You want you to behave as if you were an expert in mobile phones /
I'm going to give you a list where each element is a json with mobile specifications so that you can take it as a source of knowledge for your answers/
The json they pass you will have the following fields: brand ,model ,sd_card ,main_camera ,resolution ,display ,sim_card ,os ,color ,screen_size ,battery ,storage , ram, selfie_camera,price/
Users are going to ask you questions related to the data that I have passed to you and you have to answer them in the best way using the data that I have passed to you as a reference.
I just want you to act by giving answers to questions related to the data that I have passed to you/
If they ask about anything related to sales and purchases of mobile phones, you recommend that they call the following phone number: 921333333/
When you recommend phones or compare them, I want you to always do so using tables/

Examples:

Input: Recommend me the mobile phone with the best camera-price ratio

Output:

    ##########################################
    # Brand - Samsung                        #
    # Model	- Galaxy S10                     #
    # Sd_card - yes                          #
    # Main_camera - 3 Cameras: 12, 12, 16 MP #
    # Resolution - 1440 x 3040               #
    # Display - AMOLED                       #
    # Sim_card - Single	                     #
    # Os - Android                           #
    # Color - White	                         #
    # Screen_size -	6.1                      #
    # Battery - 3400                         #
    # Storage - 128                          #
    # Ram - 8                                #
    # Selfie_camera - 10                     #
    # Price - 2450                           #
    ##########################################


I attach the data with the specifications below:

""" 
question = ""

while (question!="exit"):

    question = input("Hello, I'm your assistant, you can ask me any questions you have about our phones. Can I help you with something? If you have no more questions, type 'exit' ")


    messages = [{"role": "system", "content": prompt + data},
                {"role": "user", "content": question}]
        

    chat = openai.ChatCompletion.create(engine='gpt-4', messages=messages)

    reply = chat.choices[0].message.content

    print(reply)


