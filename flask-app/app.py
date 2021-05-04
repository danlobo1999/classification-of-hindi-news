import os
from flask import Flask, request, render_template

app = Flask(__name__, template_folder="templates")

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Upload API
@app.route('/', methods=['POST'])
def my_form_post():
    output_text = request.form['text']
    print(output_text)
    return render_template("index.html", output_text=output_text)

# if __name__ == "__main__":
#     app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=True)