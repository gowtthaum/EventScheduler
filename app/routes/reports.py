from flask import Blueprint, render_template,Response
from app.models import  Resource,EventResourceAllocation 
from datetime import datetime
reports_bp = Blueprint("reports", __name__, url_prefix="/reports")


@reports_bp.route("/utilisation")
def utilisation():

    allocations = (
        EventResourceAllocation.query
        .join(EventResourceAllocation.event)
        .join(EventResourceAllocation.resource)
        .order_by(EventResourceAllocation.start_time)
        .all()
    )

    return render_template(
        "reports/utilisation.html",
        allocations=allocations
    )
@reports_bp.route("/utilisation/export")
def export_utilisation():

    def generate():
        yield "Resource,Event,Start Time,End Time,Hours\n"

        allocations = EventResourceAllocation.query.all()

        for alloc in allocations:
            start = alloc.start_time or alloc.event.start_time
            end = alloc.end_time or alloc.event.end_time

            if not start or not end:
                continue

            hours = (end - start).total_seconds() / 3600

            yield (
                f"{alloc.resource.name},"
                f"{alloc.event.title},"
                f"{start},"
                f"{end},"
                f"{round(hours,2)}\n"
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=resource_utilisation.csv"
        }
    )
@reports_bp.route("/debug/allocations")
def debug_allocations():
    allocations = EventResourceAllocation.query.all()
    return {
        "count": len(allocations),
        "data": [
            {
                "event": a.event.title if a.event else None,
                "resource": a.resource.name if a.resource else None,
                "start": str(a.start_time),
                "end": str(a.end_time)
            }
            for a in allocations
        ]
    }
