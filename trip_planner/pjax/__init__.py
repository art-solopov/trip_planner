from flask import Blueprint, request, render_template

from .. import csrf, db
from ..shared import user_required
from ..geocode.forms import GeocodeForm
from ..geocode.data import geocode as geocode_op


pjax = Blueprint('pjax', __name__, url_prefix='/pjax')


@pjax.route('/geocode', methods=('POST',))
@csrf.exempt
@user_required
def geocode():
    form = GeocodeForm(request.form)
    gc = geocode_op(
        form,
        country_code=request.args.get('country_code', None)
        )
    return render_template('pjax/geocode_results.html', result=gc)


@pjax.route("/map_pointer", defaults={'latlon': (51.48, 0)})
@pjax.route("/map_pointer/<decimal_pair:latlon>")
@user_required
def map_pointer(latlon):
    lat, lon = latlon
    return render_template('pjax/map_pointer.html',
                           center_lat=lat, center_lon=lon)
