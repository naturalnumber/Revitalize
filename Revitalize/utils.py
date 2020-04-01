import logging
from django.utils import timezone
from django.utils.datetime_safe import datetime, date, time

logger = logging.getLogger(__name__)
__context = 'utils.'
__tracing = True


def transfer_exception_details(e: BaseException, data: dict):
    __method = __context + 'transfer_exception_details'
    if __tracing: logger.info(__method + f"({e}, {data})")

    if e is None or data is None:
        return

    data['type'] = e.__class__.__name__

    direct_transfer = ['user_message', 'value', 'detail']

    for k in direct_transfer:
        if hasattr(e, k):
            v = getattr(e, k)
            if v is not None:
                data[k] = v

    if hasattr(e, '__cause__') and e.__cause__ is not None:
        c: BaseException = e.__cause__
        data['cause'] = c.__class__.__name__


def recursive_exception_parse(e: BaseException, data: dict):
    __method = __context + 'recursive_exception_parse'
    if __tracing: logger.info(__method + f"({e}, {data})")

    transfer_exception_details(e, data)

    cause = e.__cause__
    parent = data
    while cause is not None:
        cause_data = {}

        transfer_exception_details(cause, cause_data)

        parent['cause_data'] = cause_data

        cause = cause.__cause__
        parent = cause_data


def parse_datetime(data: dict, key: str = None, style: str = None, prefix: bool = False, pad_up: bool = False,
                   *args, **kwargs) -> datetime:
    __method = __context + 'parse_datetime'
    if __tracing: logger.info(__method + f"({data}, {key}, {style}), {prefix}, {args}, {kwargs}")

    if data is None:
        return None

    all_styles = ['iso_datetime', 'iso_date', 'UTC', 'multi']
    tried = {}

    order = []
    if style is not None: order.append(style)
    order.extend(all_styles)

    parsed_date = None

    if key is None:
        date_key = 'date'
    elif prefix:
        date_key = key + 'date'
    else:
        date_key = key

    date_value = data[key] if key in data.keys() else None

    for s in order:
        if s not in tried.keys():
            if s is 'multi':
                year_key = 'year'
                if prefix: year_key = key + year_key

                if year_key in data.keys():
                    keys = ['year', 'month', 'day', 'hour', 'minute', 'second']
                    lows = {'month': 1, 'day': 1, 'hour': 0, 'minute': 0, 'second': 0}
                    highs = {'month': 12, 'day': 28, 'hour': 23, 'minute': 59, 'second': 59}

                    values = {}

                    bad = False

                    for k in keys:
                        if prefix: k = key + k

                        v = highs[k] if pad_up else lows[k]

                        try:
                            if k in data.keys():
                                v = data[k]
                                values[k] = v if isinstance(v, int) or isinstance(v, float) else \
                                    float(v) if v.find(".") >= 0 else int(v)
                            else:
                                values[k] = v
                        except:
                            values[k] = v

                    parsed_date = None if bad else timezone.datetime(**values)

            else:
                if s in tried.keys():
                    continue
                if date_value is None:
                    tried[s] = date_key

                try:
                    temp = None
                    if s is 'iso_datetime':
                        temp = timezone.datetime.fromisoformat(date_value)
                    elif s is 'iso_date':
                        pad = time(hour=23, minute=59, second=59) if pad_up else time(hour=0, minute=0, second=0)
                        temp = timezone.datetime.combine(date.fromisoformat(date_value), pad)
                    elif s is 'UTC':
                        temp = timezone.datetime.strptime(date_value, '%Y-%m-%dT%H:%M:%SZ')

                    parsed_date = temp.replace(tzinfo=timezone.utc) if temp is not None else None
                except Exception as e:
                    parsed_date = None
                    if __tracing: logger.info(__method + f": unable to parse {date_value} using {s} because of {e}")

            if parsed_date is not None:
                return parsed_date


# This class is just a helper for dealing with some Django features quickly during development
# and will at some point be removed. Please ignore.
class ModelHelper:
    model_fields: dict = {}
    model_sorts: dict = {}
    model_displays: dict = {}
    model_filter_ons: dict = {}
    model_search_ons: dict = {}
    model_do_not_serializes: dict = {}
    model_text_types: dict = {}
    model_foreigns: dict = {}

    admin_to_register: list = []

    dicts = [model_fields, model_sorts, model_displays, model_filter_ons, model_search_ons, model_do_not_serializes,
             model_text_types, model_foreigns]

    @classmethod
    def inherit(cls, parent, child):
        for d in cls.dicts:
            if parent in d.keys():
                d[child] = d[parent].copy()
            else:
                if d is cls.model_fields:
                    d[child] = []
                else:
                    d[child] = {}

    @classmethod
    def get_(cls, dic: dict, key):
        if key not in dic.keys():
            if dic is cls.model_fields:
                dic[key] = []
            else:
                dic[key] = {}
        return dic[key]

    @classmethod
    def register(cls, model, field, priority, to_display=True, to_filter=False, to_search=False, to_serialize=True,
                 text_type=None, foreign=None):
        model_fields: list = cls.get_(cls.model_fields, model)
        model_sorts: dict = cls.get_(cls.model_sorts, model)
        model_displays: dict = cls.get_(cls.model_displays, model)
        model_filter_ons: dict = cls.get_(cls.model_filter_ons, model)
        model_search_ons: dict = cls.get_(cls.model_search_ons, model)
        model_do_not_serializes: dict = cls.get_(cls.model_do_not_serializes, model)
        model_text_types: dict = cls.get_(cls.model_text_types, model)
        model_foreigns: dict = cls.get_(cls.model_foreigns, model)

        model_fields.append(field)
        model_sorts[field] = priority
        model_displays[field] = to_display
        model_filter_ons[field] = to_filter
        model_search_ons[field] = to_search
        model_do_not_serializes[field] = not to_serialize
        model_text_types[field] = text_type
        model_foreigns[field] = foreign

    @classmethod
    def to_admin(cls, model):
        cls.admin_to_register.append(model)

    @classmethod
    def serialize(cls, model):
        if not isinstance(model, str):
            key = model.__name__
        else:
            key = model

        model_fields: list = cls.get_(cls.model_fields, key)
        model_sorts: dict = cls.get_(cls.model_sorts, key)
        model_do_not_serializes: dict = cls.get_(cls.model_do_not_serializes, key)
        model_text_types: dict = cls.get_(cls.model_text_types, key)
        model_foreigns: dict = cls.get_(cls.model_foreigns, key)

        temp = [f for f in model_fields if not model_do_not_serializes[f]]

        temp.sort(key=lambda x: model_sorts[x], reverse=True)

        return temp