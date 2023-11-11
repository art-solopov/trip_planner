from trip_planner.models import PointTypes
from trip_planner.trips.presenters import PointPresenter


def test_point_presenter_colors():
    assert PointPresenter.POINT_COLORS.keys() == set(PointTypes)
