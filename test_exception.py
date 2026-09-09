valid_int: bool = False
user_int: str = ""

while not valid_int :
    user_input = input("Entrer un nombre : ")
    try : 
        user_int = int(user_input)
    except ValueError : 
        print("pas un nombre")
    else :
        valid_int = True

### Ask the user to choose a filename n articles/
### Print its content, if the file does not exist, ask the user again, using try and except