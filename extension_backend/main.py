from fastapi import FastAPI
from utility import utils
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel
from prompts.prompt import main_prompt
class input(BaseModel):
    text: str 

app = FastAPI()

#TODO: Add CORS
#Put APIS logic else where
#TODO: User Authentication and JWT

@app.post('/')
def homepage():
    return {"Sucess"}

@app.post('/summarize')
def summarize():
    #TODO: LLama3 support 
    
    #Configuration
    config_file_path = r"C:\Users\HARSHAD BHUSARE\Desktop\Chrome Extension\extension_backend\config\models.yaml"
    config = utils.read_yaml(config_file_path)
    for model_config in config['models']:
        print(model_config['name'])
        if model_config["name"] == "OpenAI":
            model = model_config['model']
            key = model_config['key']

    #print(f"Question from human: {question}")
    question = "The office of shogun was in practice hereditary, although over the course of the history of Japan several different clans held the position. The title was originally held by military commanders during the Heian period in the eighth and ninth centuries. When Minamoto no Yoritomo gained political ascendency over Japan in 1185, the title was revived to regularize his position, making him the first shogun in the usually understood sense."
    
    template = main_prompt.format(text="text")
    print(template)
    prompt = PromptTemplate.from_template(template)
    print('Reached control')

    llm = OpenAI(model=model, openai_api_key=key)
    llm_chain = prompt | llm
    res =""
    try:
        res = llm_chain.invoke(question)
        print(res)
    except Exception as e:
        print(e)
    
    return {"response": res}
