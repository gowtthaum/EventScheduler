from app.models import EventResourceAllocation, Event
from app.models import Resource, EventResourceAllocation, Event

def check_conflict(resource_id, start, end):
    allocations = EventResourceAllocation.query.filter_by(resource_id=resource_id).all()

    for allocation in allocations:
        event = Event.query.get(allocation.event_id)

        # Overlap condition
        if start < event.end_time and end > event.start_time:
            return True

    return False
def suggest_available_resources(resource_type, start, end):
    suggestions = []

    resources = Resource.query.filter_by(
        resource_type=resource_type
    ).all()

    for resource in resources:
        allocations = EventResourceAllocation.query.filter_by(
            resource_id=resource.resource_id
        ).all()

        conflict = False
        for alloc in allocations:
            event = Event.query.get(alloc.event_id)
            if event and start < event.end_time and end > event.start_time:
                conflict = True
                break

        if not conflict:
            suggestions.append(resource.resource_name)

    return suggestions
def has_time_conflict(existing_start, existing_end, new_start, new_end):
    return not (new_end <= existing_start or new_start >= existing_end)
