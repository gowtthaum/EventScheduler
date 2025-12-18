from flask import Blueprint, render_template
from app.models import EventResourceAllocation

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')

@reports_bp.route('/')
def utilisation():
    allocations = EventResourceAllocation.query.all()
    return render_template(
        'reports/utilisation.html',
        allocations=allocations
    )
