from flask import Blueprint, render_template
from app.models import Event, Resource, EventResourceAllocation

home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():

    total_events = Event.query.count()
    total_resources = Resource.query.count()
    total_allocations = EventResourceAllocation.query.count()

    utilisation = []

    resources = Resource.query.all()
    for resource in resources:
        allocations = EventResourceAllocation.query.filter_by(
            resource_id=resource.id
        ).all()

        total_hours = 0
        for alloc in allocations:
            if alloc.start_time and alloc.end_time:
                total_hours += (
                    alloc.end_time - alloc.start_time
                ).total_seconds() / 3600

        utilisation.append({
            "resource": resource.name,
            "hours": round(total_hours, 2)
        })

    return render_template(
        "home.html",
        total_events=total_events,
        total_resources=total_resources,
        total_allocations=total_allocations,
        utilisation=utilisation
    )
