from flask import Blueprint, render_template
from markupsafe import Markup, escape

from ..shared import user_required
from ..models import Point
from .data import PointData


points = Blueprint('points', __name__, url_prefix='/points')


def render_weekday(weekday: str) -> str:
    wday_short = weekday[0:3]
    return Markup(f'<span class="{wday_short.lower()}">{escape(weekday)}</span>')


points.add_app_template_filter(render_weekday, 'wday')


@points.route("/<int:id>")
@user_required
def show(id: int):
    point = Point.query.get_or_404(id)
    data = PointData(point)
    return render_template('points/show.html', point=point,
                           data=data)
