from bs4 import BeautifulSoup

#Data Preprocessing
class data_preprocessor:
    def __init__(self, raw_data):
        self.raw_data = raw_data
        self.path = r"./data/ref2.html"
        
    def nothing(self):
        print("nothing")

    def write_html_data(self):
        file_path = r"./data/ref2.html"
        with open(self.path, "w", encoding="utf-8", errors="replace") as f:
            f.write(self.raw_data)
            print('written')
            
    def read_html(self):
        with open(self.path, "r", encoding="utf-8", errors="replace") as f:
            html = f.read()    
        return html 
    
    @staticmethod    
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
        print(text)
        if len(text) <= 30000:
            return text
        else:
            #TODO: Write a proper chuncking logic and add a vector database
            return text[:30000]
                     
                    
    