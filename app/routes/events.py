from flask import Blueprint, render_template, request, redirect, url_for
from app.models import db, Event,Resource
from datetime import datetime

events_bp = Blueprint('events', __name__, url_prefix='/events')
def suggest_resources(event_title):
    title = event_title.lower()

    if "meeting" in title or "review" in title:
        return ["Meeting Room", "Projector"]
    elif "seminar" in title or "presentation" in title:
        return ["Seminar Hall", "Microphone", "Projector"]
    elif "training" in title or "workshop" in title:
        return ["Training Room", "Laptop", "Whiteboard"]
    else:
        return ["Conference Room"]


@events_bp.route('/')
def list_events():
    events = Event.query.all()
    return render_template('events/list.html', events=events)


@events_bp.route('/create', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form['title']

        event = Event(
            title=title,
            start_time=datetime.strptime(
                request.form['start_time'], "%Y-%m-%dT%H:%M"
            ),
            end_time=datetime.strptime(
                request.form['end_time'], "%Y-%m-%dT%H:%M"
            )
        )
        db.session.add(event)
        db.session.commit()

        # 🔥 AUTO RESOURCE SUGGESTION
        suggested_resources = suggest_resources(title)

        for res_name in suggested_resources:
            existing = Resource.query.filter_by(name=res_name).first()
            if not existing:
                db.session.add(Resource(name=res_name))

        db.session.commit()

        return redirect(url_for('events.list_events'))

    return render_template('events/form.html')

@events_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_event(id):
    event = Event.query.get_or_404(id)

    if request.method == 'POST':
        event.title = request.form['title']
        event.start_time = datetime.strptime(
            request.form['start_time'], "%Y-%m-%dT%H:%M"
        )
        event.end_time = datetime.strptime(
            request.form['end_time'], "%Y-%m-%dT%H:%M"
        )
        db.session.commit()
        return redirect(url_for('events.list_events'))

    return render_template('events/form.html', event=event)

@events_bp.route('/delete/<int:id>')
def delete_event(id):
    event = Event.query.get_or_404(id)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('events.list_events'))
@events_bp.route('/home')
def home():
    return redirect(url_for('events.list_events'))