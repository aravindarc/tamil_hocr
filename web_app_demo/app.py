import sys

# including path to the ocr_engine
# or simply copy ocr_engine to this dir
sys.path.insert(0, './..')      

# this is our OCR engine
import ocr_engine as ocr_eng    

from flask import Flask, request, render_template, jsonify, send_from_directory
from base64 import b64decode
import os
import numpy as np
import codecs

app = Flask(__name__)
app.config['UPLOADS_DIR'] = "uploads"
app.config['ASSETS_DIR'] = "assets"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/assets/<filename>")
def get_assets(filename):
    print("Client asked asset file " + filename)
    return send_from_directory(app.config['ASSETS_DIR'], filename)

@app.route("/uploads/<filename>")
def get_file_from_uploads(filename):
    print("Client asked uploaded file " + filename)
    return send_from_directory(app.config["UPLOADS_DIR"], filename)

@app.route("/upload", methods=["POST"])
def upload():
    letter = '-'
    data = str(request.data).split(',')[1]
    content = b64decode(data) 
    file = open(app.config['UPLOADS_DIR'] + "/image.png", 'wb+')

    # the drawing file is written into the uploads dir as a image.png
    file.write(content)     
                            
    file.close()

    # the path of the file is passed to the engine
    result = ocr_eng.recognize(app.config['UPLOADS_DIR'] + "/image.png")

    # the file is deleted
    os.remove(app.config['UPLOADS_DIR'] + "/image.png")

    # the output is sent to the webpage
    return jsonify({"letter": tamil_letters[result]})                       

if __name__ == "__main__":
    
    # the recognition will be a int from 0 to 246,
    # to map these numbers into tamil characters
    #a csv file with all the characters is present
    filename = 'label_map.csv'  
                                
    with codecs.open(filename, 'r', encoding = 'utf-8') as f:
        tamil_letters = np.loadtxt(f, dtype=str, delimiter=',')
    tamil_letters = tamil_letters.ravel()
    
    app.run(debug = False, host = '0.0.0.0')
