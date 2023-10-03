from flask import Flask,request,jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from data import *
import chardet

app = Flask(__name__)  # Initialize Flask App
CORS(app)

FILES='FILES'
if not os.path.exists(FILES):
    os.makedirs(FILES)

app.config['FILES'] = FILES

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if request.method == 'POST':
            if 'file' not in request.files:
                 return jsonify({"Error Status": "File does not exist"})
            else:
                file = request.files['file']
                if file.filename == '':
                    return jsonify({"Error Status": "File not selected"})
                if file:
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['FILES'],filename)
                    file.save(file_path)
                    
                    result=processing(file_path)
                    return jsonify(result)
                
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(debug=True)