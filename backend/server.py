from flask import Flask
import summerise as summerise
from flask import Flask, flash, redirect, render_template, request, session, abort, send_file
import os
 
app = Flask(__name__)
 
@app.route('/')
def parameterExtraction():
    if request.method == 'GET':
        parsed_url = request.args['link']
        result = summerise.final(parsed_url)
        return send_file('IUdb-7R_summarized.mp4', as_attachment=False)


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='127.0.0.1', port=4000)
