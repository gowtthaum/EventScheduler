from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from app.models import db, Resource, Event


resources_bp = Blueprint('resources', __name__, url_prefix='/resources')


@resources_bp.route('/', methods=['GET', 'POST'])
def list_resources():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            existing = Resource.query.filter_by(name=name).first()
            if not existing:
                db.session.add(Resource(name=name))
                db.session.commit()
        return redirect(url_for('resources.list_resources'))

    resources = Resource.query.all()
    events = Event.query.all()
    return render_template('resources/list.html', resources=resources, events=events)

@resources_bp.route('/delete/<int:id>')
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return redirect(url_for('resources.list_resources'))
 
 
 #🔹 RESOURCE SUGGESTION LOGIC

def suggest_resources(event_title):
    title = event_title.lower()

    if "meeting" in title or "review" in title or "standup" in title:
        return ["Meeting Room", "Projector", "Whiteboard"]

    
    elif "training" in title or "workshop" in title:
        return ["Training Room", "Laptop", "Whiteboard", "Projector"]

    elif "seminar" in title or "presentation" in title:
        return ["Seminar Hall", "Projector", "Microphone"]

    
    elif "conference" in title:
        return ["Conference Hall", "Projector", "Microphone", "Speaker System"]

    
    elif "new year" in title or "party" in title or "celebration" in title:
        return ["Stage", "Sound System", "Lighting", "Decorations"]

    elif "farewell" in title:
        return ["Hall", "Sound System", "Projector", "Decorations"]

    elif "birthday" in title:
        return ["Party Hall", "Cake Table", "Decorations", "Sound System"]

    
    elif "exam" in title:
        return ["Exam Hall", "Invigilator Desk", "Clock"]

    elif "convocation" in title:
        return ["Auditorium", "Stage", "Sound System", "Seating Arrangement"]


    elif "hackathon" in title:
        return ["Lab Room", "High-Speed Internet", "Power Extension"]

    elif "demo" in title:
        return ["Projector", "Laptop", "Display Screen"]

    
    elif "sports" in title or "tournament" in title:
        return ["Playground", "Scoreboard", "First Aid Kit"]

    
    elif "interview" in title:
        return ["Interview Room", "Laptop", "Evaluation Sheets"]

    else:
        return ["Venue", "Projector"]



@resources_bp.route('/suggest/<int:event_id>')
def suggest(event_id):
    event = Event.query.get_or_404(event_id)
    suggestions = suggest_resources(event.title)
    return jsonify(suggestions)