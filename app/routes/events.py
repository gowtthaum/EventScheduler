from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify

from datetime import datetime
from app.models import db, Event, EventResourceAllocation

events_bp = Blueprint('events', __name__, url_prefix='/events')


# 📌 LIST EVENTS + ADD FORM + EDIT FORM
@events_bp.route('/', methods=['GET'])
def list_events():
    events = Event.query.all()
    edit_event = None

    edit_id = request.args.get('edit')
    if edit_id:
        edit_event = Event.query.get(int(edit_id))

    return render_template(
        'events/list.html',
        events=events,
        edit_event=edit_event
    )


# 📌 CREATE EVENT
@events_bp.route('/create', methods=['POST'])
def create_event():
    title = request.form.get('title')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')

    start_time = datetime.strptime(start_time, '%Y-%m-%dT%H:%M')
    end_time = datetime.strptime(end_time, '%Y-%m-%dT%H:%M')

    event = Event(title=title, start_time=start_time, end_time=end_time)
    db.session.add(event)
    db.session.commit()

    flash('Event added successfully', 'success')
    return redirect(url_for('events.list_events'))


# 📌 UPDATE EVENT
@events_bp.route('/update/<int:event_id>', methods=['POST'])
def update_event(event_id):
    event = Event.query.get_or_404(event_id)

    event.title = request.form.get('title')
    event.start_time = datetime.strptime(
        request.form.get('start_time'), '%Y-%m-%dT%H:%M'
    )
    event.end_time = datetime.strptime(
        request.form.get('end_time'), '%Y-%m-%dT%H:%M'
    )

    db.session.commit()
    flash('Event updated successfully', 'success')
    return redirect(url_for('events.list_events'))

@events_bp.route('/delete/<int:event_id>', methods=['GET', 'POST'])
def delete_event(event_id):
    # delete allocations first
    EventResourceAllocation.query.filter_by(event_id=event_id).delete()

    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()

    flash('Event deleted successfully', 'success')
    return redirect(url_for('events.list_events'))

@events_bp.route('/api')
def events_api():
    events = Event.query.all()

    data = []
    for event in events:
        data.append({
            "id": event.id,
            "title": event.title,
            "start": event.start_time.isoformat(),
            "end": event.end_time.isoformat() if event.end_time else None
        })
        return jsonify(data)

@events_bp.route('/calendar')
def calendar_view():
    return render_template('events/calendar.html')

