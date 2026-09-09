from pathlib import Path
from methods import *
def askarticle():
    valid_name = False
    while not valid_name :
        try : 
            name_input = input("choisissez un nom d'article dans articles : ")
            file_input = lire_article(name_input)
            print(file_input.content)
        except HTTPException :
            print("incorrect")
        else : 
            valid_name = True

askarticle()

def show_article():
    ask_again = True
    content = ""
    while ask_again :
        fname = input("Enter article name")
        file_path = Path("../../../1_blog/articles")/(fname+".md")
        try :
            content = file_path.read_text()
        except FileNotFoundError :
            print("Invalid filename")
        else : 
            ask_again = False
    print(content)

show_article()