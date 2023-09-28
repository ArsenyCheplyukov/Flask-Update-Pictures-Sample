#Local
from app import app
#Started
import os
# VirtualEnv
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template, Response
from base64 import b64encode
import base64
from io import BytesIO #Converts data from Database into byte
from PIL import Image

from flask_sqlalchemy import SQLAlchemy

#resolution setting


#set sqlalchemy database
db = SQLAlchemy()

# Function that initializes the db and creates the tables
def db_init(app):
    db.init_app(app)
    # Creates the tables if the db doesnt already exist
    with app.app_context():
        db.create_all()

class Img(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=False)
    name = db.Column(db.Text, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    def __repr__(self):
        return f'Pic Name: {self.name} Data: {self.img}'

db_init(app)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)
        files = request.files.getlist('files[]')
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                img = Img(img=base64.b64encode(file.read()).decode('ascii'), name=filename, mimetype=file.mimetype)
                db.session.add(img)
                db.session.commit()
    return render_template('upload.html', img_data=Img.query.all())

@app.route('/<int:id>')
def get_img(id):
    img = Img.query.filter_by(id=id).first()
    if not img:
        return 'Img Not Found!', 404
    return Response(img.img, mimetype=img.mimetype)

# to select multiple files, you should hold 
if __name__ == "__main__":
    app.run()