import os
import sys
from flask import Flask, request, render_template

sys.path.append(os.path.abspath("../"))

from hindibert.classify import Classify

app = Flask("flask-app", template_folder="templates")


# Home page
@app.route("/")
def index():
    return render_template("index.html")


# Upload API
@app.route("/classify/", methods=["POST", "GET"])
def classify():
    if request.method == "POST":
        hindi_bert = Classify()
        input_text = [request.form.get("data")]
        output_text = "Category : " + hindi_bert.predictor(text=input_text)
        del hindi_bert

        return output_text

    return render_template("index.html", output_text=output_text)


if __name__ == "__main__":
    # app.run(debug=True, use_reloader=True)
    app.run()
