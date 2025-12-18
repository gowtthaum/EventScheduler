from flask import Blueprint, render_template
from sqlalchemy import func

from app.models import db, Event, Resource, EventResourceAllocation

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def dashboard():

    total_events = Event.query.count()
    total_resources = Resource.query.count()
    total_allocations = EventResourceAllocation.query.count()

    utilisation = (
        db.session.query(
            Resource.name.label("name"),
            func.count(EventResourceAllocation.id).label("hours")
        )
        .join(EventResourceAllocation, Resource.id == EventResourceAllocation.resource_id)
        .group_by(Resource.name)
        .all()
    )

    return render_template(
        "home.html",
        total_events=total_events,
        total_resources=total_resources,
        total_allocations=total_allocations,
        utilisation=utilisation
    )
@home_bp.route('/')
def home():
    return render_template(
        'dashboard.html',
        total_events=Event.query.count(),
        total_resources=Resource.query.count(),
        total_allocations=EventResourceAllocation.query.count()
    )