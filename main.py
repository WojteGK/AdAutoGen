from tkinter import Tk
from tkinter.filedialog import askopenfilename
import http.client
import json
import os

def get_file_path():
    Tk().withdraw() # to hide the main window
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = askopenfilename(initialdir=current_dir) # show an "Open" dialog box and return the path to the selected file
    return file_path

    # reszta twojego kodu
def read_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return data

def generate_car_description(car_data):
    # convert car data to a format that can be understood by the API
    text = f"Brand: {car_data['brand']}\nModel: {car_data['model']}\nYear of production: {car_data['year']}\nColor: {car_data['color']}"

    # create a connection
    conn = http.client.HTTPSConnection("api.openai.com")

    # send a request to the API
    payload = json.dumps({
        'prompt': text,
        'max_tokens': 100,
        'temperature': 0.7,
        'n': 1,
        'stop': '\n'
    })
    headers = {'Authorization': 'Bearer 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', 'Content-Type': 'application/json'}
    conn.request("POST", "/v1/engines/davinci-codex/completions", payload, headers)

    # get the response from the API
    res = conn.getresponse()
    data = res.read()

    # parse the response from the API
    response_data = json.loads(data.decode("utf-8"))

    # return the generated description
    return response_data['choices'][0]['text'].strip()

def save_car_description(description, file_path):
    # save the description to a file
    with open(file_path, 'w') as file:
        file.write(description)


if __name__ == "__main__":
    file_path = get_file_path()
    car_data = read_file(file_path)
    description = generate_car_description(car_data)
    save_car_description(description, file_path)