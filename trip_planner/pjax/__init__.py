from flask import Blueprint, request, render_template

from .. import csrf
from ..shared import user_required
from ..geocode.forms import GeocodeForm
from ..geocode.data import geocode as geocode_op


pjax = Blueprint('pjax', __name__, url_prefix='/pjax')


@pjax.route('/geocode', methods=('POST',))
@csrf.exempt
@user_required
def geocode():
    form = GeocodeForm(request.form)
    results = geocode_op(
        form,
        country_code=request.args.get('country_code', None)
        )
    return render_template('pjax/geocode_results.html', results=results)
