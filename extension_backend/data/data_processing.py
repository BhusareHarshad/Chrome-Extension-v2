from bs4 import BeautifulSoup
import os

PATH = "./data/ref.html"

#Data Preprocessing
class data_preprocessor:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        
    def write_html_data(self):
        try:
            with open(PATH, "w", encoding="utf-8", errors="replace") as f:
                f.write(self.raw_data)
        except FileNotFoundError as fe:
            print(fe)
            
                        
    def read_html(self):
        with open(PATH, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()    
        return html 
     
    def extract_html_data(self):
        
        html = self.read_html()
        soup = BeautifulSoup(html)

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)
        if len(text) <= 3000:
            return text
        else:
            #TODO: Write a proper chuncking logic and add a vector database
            return text[:3000]
                     