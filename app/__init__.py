from app.exceptions import ConflictEmailError, InvalidTypeError
from os import environ, path, makedirs, walk, path 
from flask import Flask, request
from ujson import dump, load
from environs import Env

app = Flask(__name__)

env = Env()
env.read_env()
DATA_DIR = environ.get('DATABASE_DIRECTORY')

if not path.exists(DATA_DIR):
    makedirs(DATA_DIR)

@app.get('/user')
def get_data():    
    for _, _, files in walk(DATA_DIR):
        if not 'database.json' in files:
            with open(f'{DATA_DIR}/database.json', 'w') as json_file:
                dump({"data": []}, json_file, indent=4)
                
    with open(f'{DATA_DIR}/database.json', 'r') as json_file:
        data = load(json_file)
        return data, 200

@app.post('/user')
def save_data():
    req = request.get_json()
    name = req["nome"]
    email = req["email"]
    
    try:
        if type(name) != str or type(email) != str:
            raise InvalidTypeError(name, email)

        name = name.title()
        email = email.lower()

        user_obj = {
            "nome": name,
            "email": email,
            "id": 1
        }

        for _, _, files in walk(DATA_DIR):
            if not 'database.json' in files:
                with open(f'{DATA_DIR}/database.json', 'w') as json_file:
                    dump({"data": []}, json_file, indent=4)

        with open(f'{DATA_DIR}/database.json', 'r') as json_file:
            data = load(json_file)

        for user in data["data"]:
            if user["email"] == email:
                raise ConflictEmailError
            
        if len(data["data"]) > 0:
            last_id = data["data"][-1]["id"]
            user_obj["id"] = last_id + 1

        data["data"].append(user_obj)

        with open(f'{DATA_DIR}/database.json', 'w') as json_file:
            dump(data, json_file, indent=4)

        data = {"data": user_obj}
        
        return data, 201

    except InvalidTypeError as error:
        return error.message, 400

    except ConflictEmailError as error:
        return error.message, 409