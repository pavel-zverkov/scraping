import datetime
from json import JSONEncoder

from ...mos_season_results.web_parser.control_point_info import ControlPointInfo

from ...constants import Constants


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, ControlPointInfo):
            return obj.__dict__
        if type(obj) == datetime.time:
            return obj.strftime(Constants.TIME_FORMAT)
        elif type(obj) == datetime.date:
            return obj.strftime(Constants.DATE_FORMAT)
        elif type(obj) == datetime.datetime:
            return obj.strftime(Constants.DATETIME_FORMAT)
