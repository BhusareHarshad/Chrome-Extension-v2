from fastapi import FastAPI
from utility import utils
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel
from prompts.prompt import main_prompt
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import BSHTMLLoader
from db_utils import db
from bs4 import BeautifulSoup
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

#Put APIS logic else where
#TODO: User Authentication and JWT

@app.get('/')
def homepage():
    return {"Sucess"}

@app.post('/summarize')
async def summarize(htmldata: SummaryRequest):
    #TODO: LLama3 support
    
    #Configuration
    config_file_path = r"config\models.yaml"
    config = utils.read_yaml(config_file_path)
    for model_config in config['models']:
        if model_config["name"] == "OpenAI":
            model = model_config['model']
            key = model_config['key']
            
    #TODO: Put it in different python file and class
    file_path = r"./data/ref2.html"
    def write_html_data(data):
        with open(file_path, "w", encoding="utf-8", errors="replace") as f:
            f.write(data)
            
    def read_html():
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()    
        return html 
  
    def extract_html_data():
        
        html = read_html()
        soup = BeautifulSoup(html)

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        print(text)
        if len(text) < 3000:
            return text
        else:
            #TODO: Write a proper chuncking logic and add a vector database
            return text[:3000]
    
    write_html_data(htmldata.htmldata)
    question = extract_html_data()
    print(f"Question: {question}")
    
    #prompt Template and llm calls
    template = main_prompt.format(text="text")
    prompt = PromptTemplate.from_template(template)
    print('Reached control')

    llm = OpenAI(model=model, openai_api_key=key)
    llm_chain = prompt | llm
    res =""
    try:
        res = llm_chain.invoke(question)
        print(res)
        #TODO: Feedback functionality at frontend
        await db.insert_data(htmldata.htmldata, res, "positive")
    except Exception as e:
        logging.error("Error while connecting to PostgreSQL: %s", e)
        print(e)
    
    return {"data": res}
