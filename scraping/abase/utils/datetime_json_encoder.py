import datetime
from json import JSONEncoder

from ...constants import Constants


class DateTimeEncoder(JSONEncoder):
    # Override the default method
    def default(self, obj):
        if type(obj) == datetime.date:
            print('date')
            return obj.strftime(Constants.DATE_FORMAT)
        elif type(obj) == datetime.datetime:
            print('datetime')
            return obj.strftime(Constants.DATETIME_FORMAT)
