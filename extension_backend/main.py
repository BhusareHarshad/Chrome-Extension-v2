from fastapi import FastAPI
from utility import utils
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAI
from pydantic import BaseModel
from prompts.prompt import main_prompt
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.document_loaders import BSHTMLLoader

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this to restrict origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

class input(BaseModel):
    text: str 
    
class SummaryRequest(BaseModel):
    htmldata: str

#Put APIS logic else where
#TODO: User Authentication and JWT

@app.get('/')
def homepage():
    return {"Sucess"}

@app.post('/summarize')
def summarize(htmldata: SummaryRequest):
    #TODO: LLama3 support 
    print(htmldata.htmldata)
    #Configuration
    config_file_path = r"config\models.yaml"
    config = utils.read_yaml(config_file_path)
    for model_config in config['models']:
        if model_config["name"] == "OpenAI":
            model = model_config['model']
            key = model_config['key']
            
    with open("ref.html", "w", encoding='utf-8', errors="replace") as f:
        f.write(htmldata.htmldata)
        
    with open("ref.txt", 'w', encoding='utf-8', errors="replace") as ff:
        ff.write(htmldata.htmldata)


    #print(f"Question from human: {question}")
    question = "The office of shogun was in practice hereditary, although over the course of the history of Japan several different clans held the position. The title was originally held by military commanders during the Heian period in the eighth and ninth centuries. When Minamoto no Yoritomo gained political ascendency over Japan in 1185, the title was revived to regularize his position, making him the first shogun in the usually understood sense."
    loader = BSHTMLLoader('ref.html')
    data = loader.load()
    
    for dat in data:
        question = dat.page_content
    
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
    
    return {"data": res}
