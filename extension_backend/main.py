from fastapi import FastAPI
from utility import utils
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel
from prompts.prompt import main_prompt, qna, main_prompt2
from fastapi.middleware.cors import CORSMiddleware
from db_utils.db import (
    insert_data
)
from data.data_processing import data_preprocessor
import logging

logging.basicConfig(filename='Logs/app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
  
class SummaryRequest(BaseModel):
    htmldata: str
    
class Question(BaseModel):
    htmldata: str
    question: str

#Put APIS logic else where
#TODO: User Authentication and JWT

@app.get('/')
def homepage():
    return {"Response": "Success"}

@app.post('/summarize')
async def summarize(htmldata: SummaryRequest):
    #TODO: LLama3 support
    
    #Configuration
    config_file_path = r"config\models.yaml"
    res =""
    config = utils.read_yaml(config_file_path)
    for model_config in config['models']:
        if model_config["name"] == "OpenAI":
            model = model_config['model']
            key = model_config['key']
               
    data = data_preprocessor(htmldata.htmldata)
    data.write_html_data()
    question = data.extract_html_data()
    
    #prompt Template and llm calls
    template = main_prompt.format(text="text")
    prompt = PromptTemplate.from_template(template)
    print('Reached control')

    try:
        #TODO: llm calls put in another class file
        llm = OpenAI(model=model, openai_api_key=key)
        llm_chain = prompt | llm
        res = llm_chain.invoke(question)
        #TODO: Feedback functionality at frontend
        await insert_data(htmldata.htmldata, res, "positive")
    except Exception as e:
        logging.error("Error while generating response: %s", e)
    
    return {"data": res}


@app.post('/question')
async def qna(question: Question):
    #TODO: LLama3 support

    #Configuration
    config_file_path = r"config\models.yaml"
    res =""
    config = utils.read_yaml(config_file_path)
    for model_config in config['models']:
        if model_config["name"] == "OpenAI":
            model = model_config['model']
            key = model_config['key']
            
    data = data_preprocessor(question.htmldata)
    data.write_html_data()
    html = data.extract_html_data()
    
    #prompt Template and llm calls
    #template = qna.format(text="text", question="question")
    #template = qna.format(text="text")
    template = main_prompt2.format(text="text", res='res')
    prompt = PromptTemplate.from_template(template)
    print('Reached control')
    ques = question.question
    
    try:
        #TODO: llm calls put in another class file
        #Create a common llm calls python file
        llm = OpenAI(model=model, openai_api_key=key)
        llm_chain = prompt | llm
        res = llm_chain.invoke({"res": ques, "text": html})
        #TODO: Feedback functionality at frontend
        await insert_data(question.htmldata, res, "positive")
    except Exception as e:
        print(e)
        logging.error("Error while generating response: %s", e)
    
    return {"data": res}