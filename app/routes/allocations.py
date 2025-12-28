from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import timedelta
from app.models import db, Event, Resource, EventResourceAllocation
from app.utils.conflict_checker import has_time_conflict

allocations_bp = Blueprint("allocations", __name__, url_prefix="/allocations")

# Default duration: 1 hour per resource
ALLOCATION_DURATION = timedelta(hours=1)


@allocations_bp.route("/assign", methods=["GET", "POST"])
def assign_resources():
    events = Event.query.all()
    resources = Resource.query.all()
    allocations = EventResourceAllocation.query.all()

    if request.method == "POST":
        event_id = int(request.form["event_id"])
        resource_ids = request.form.getlist("resource_ids")

        event = Event.query.get_or_404(event_id)

        # 🔥 IMPORTANT FIX: continue after last allocation
        last_allocation = EventResourceAllocation.query.filter_by(
            event_id=event.id
        ).order_by(EventResourceAllocation.end_time.desc()).first()

        if last_allocation:
            current_start_time = last_allocation.end_time
        else:
            current_start_time = event.start_time

        for resource_id in resource_ids:
            resource = Resource.query.get_or_404(resource_id)

            start_time = current_start_time
            end_time = start_time + ALLOCATION_DURATION

            # Prevent duplicate allocation
            existing = EventResourceAllocation.query.filter_by(
                event_id=event.id,
                resource_id=resource.id
            ).first()
            if existing:
                continue

            db.session.add(
                EventResourceAllocation(
                    event_id=event.id,
                    resource_id=resource.id,
                    start_time=start_time,
                    end_time=end_time
                )
            )

            # 🔥 MOVE TIME FOR NEXT RESOURCE
            current_start_time = end_time

        db.session.commit()
        flash("Resources allocated sequentially (1 hour each)", "success")
        return redirect(url_for("allocations.assign_resources"))

    return render_template(
        "allocations/list.html",
        events=events,
        resources=resources,
        allocations=allocations
    )