from flask import Blueprint, flash, render_template, request, jsonify, send_file
from flask_login import login_required, current_user
from . import db
from .models import Midi_file, Note
import json
from .melodygenerator import SEQUENCE_LENGTH, MelodyGenerator
from io import BytesIO


# this page is a blueprint for all of our url routes - we have to register them in __init__.py
views = Blueprint('views', __name__)


@views.route('/', methods=['POST', 'GET'])
@login_required  # cant visit home page unless you are logged in
def home():
    if request.method == 'POST':
        # save the note in the database
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short !')
        else:
            # assign the note to the current user
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('note was successfully added !', category='success')

    return render_template('home.html', user=current_user)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})
        
        
    
@views.route('/generate')
def generate():
    mg = MelodyGenerator()
    seed = "55 _ _ _ 60 _ _ _ 55 _ _ _ 55 _"
    seed2 = "67 _ _ _ _ _ 65 _ 64 _ 62 _ 60 _ _ _"
    seed3 = "67 _ _ _"
    melody = mg.generate_melody(seed2, 500, SEQUENCE_LENGTH, 0.2) #melody in time series representation
    print(melody)
    mg.save_melody(melody)
    
    return '<p> Melody generated!!!! </p>'




@views.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        file = request.files['file']

        upload = Midi_file(filename=file.filename, data=file.read())
        db.session.add(upload)
        db.session.commit()

        return f'Uploaded: {file.filename}'
    
    return render_template('upload.html', user=current_user)



@views.route('/download/<upload_id>')
def download(upload_id):
    upload = Midi_file.query.filter_by(id=upload_id).first()
    return send_file(BytesIO(upload.data), attachment_filename=upload.filename, as_attachment=True)