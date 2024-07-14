from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import mimetypes
import json
import os
from dotenv import load_dotenv

load_dotenv('.env')
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")


@app.route("/", methods=["GET", "POST"])
def index():
    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        os.makedirs(app.config["UPLOAD_FOLDER"])
    message = None
    if request.method == "POST":
        file = request.files["file"]
        if is_audio_file(file.filename):
            filename = secure_filename(file.filename)
            if filename in os.listdir(app.config["UPLOAD_FOLDER"]):
                message = "File already exists"
            else:
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                message = "Upload successfully"
        else:
            message = "Non-audio file detected"
    files = sorted(os.listdir(app.config["UPLOAD_FOLDER"]))
    accept = request.headers.get("Accept", "")
    if "application/json" in accept:
        return json.dumps({"message": message, "files": files}).encode("utf-8")
    else:
        return render_template("index.html", files=files, message=message)


def is_audio_file(filename):
    mimetype, _ = mimetypes.guess_type(filename)
    return (
        filename
        and "." in filename
        and mimetype
        and mimetype.startswith("audio")
    )


if __name__ == "__main__":
    app.run(port=8888)
