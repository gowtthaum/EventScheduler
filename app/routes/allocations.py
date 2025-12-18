from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import timedelta
from app.models import db, Event, Resource, EventResourceAllocation

allocations_bp = Blueprint("allocations", __name__, url_prefix="/allocations")

ALLOCATION_DURATION = timedelta(hours=1)


@allocations_bp.route("/", methods=["GET", "POST"])
def assign_resources():
    events = Event.query.all()
    resources = Resource.query.all()

    if request.method == "POST":
        event_id = request.form.get("event_id")
        resource_id = request.form.get("resource_id")

        if not event_id or not resource_id:
            flash("Select event and resource", "danger")
            return redirect(url_for("allocations.assign_resources"))

        event = Event.query.get_or_404(event_id)

        last_allocation = (
            EventResourceAllocation.query
            .filter_by(event_id=event.id)
            .order_by(EventResourceAllocation.end_time.desc())
            .first()
        )

        start_time = last_allocation.end_time if last_allocation else event.start_time
        end_time = start_time + ALLOCATION_DURATION

        if end_time > event.end_time:
            flash("Event time exhausted", "warning")
            return redirect(url_for("allocations.assign_resources"))

        allocation = EventResourceAllocation(
            event_id=event.id,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time
        )

        db.session.add(allocation)
        db.session.commit()

        flash("Resource allocated successfully", "success")
        return redirect(url_for("allocations.assign_resources"))

    allocations = EventResourceAllocation.query.order_by(
        EventResourceAllocation.start_time
    ).all()

    return render_template(
        "allocations/list.html",
        events=events,
        resources=resources,
        allocations=allocations
    )
