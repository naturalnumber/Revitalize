from django.db.models.query import QuerySet
from django.utils.datetime_safe import datetime, date, time
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils.translation import gettext as _

from Revitalize.serializers import *
from django.utils import timezone
import pytz

# Helper methods

print_debug = True
print_debug2 = False


def _m(m: str):
    return {'message': m}


def _r(m: str, s: status):
    return Response(_m(m), s)


def _ok(m: str):
    return Response(_m(m), status.HTTP_200_OK)


def _bad(m: str):
    return Response(_m(m), status.HTTP_400_BAD_REQUEST)


def _ex(e: BaseException, data: dict):
    if e is None or data is None:
        return

    #data['exception'] = e.
    data['type'] = e.__class__.__name__

    #if hasattr(e, '__traceback__') and e.__traceback__ is not None:
    #    data['trace'] = e.__traceback__.

    if hasattr(e, 'user_message') and e.user_message is not None:
        data['user_message'] = e.user_message

    if hasattr(e, 'value') and e.value is not None:
        data['bad_value'] = e.value

    if hasattr(e, '__cause__') and e.__cause__ is not None:
        c: BaseException = e.__cause__
        data['cause'] = c.__class__.__name__

    if hasattr(e, 'detail'):
        data['detail'] = e.detail


def _recursive_exception_parse(e: BaseException, data: dict):
    _ex(e, data)

    cause = e.__cause__
    parent = data
    while cause is not None:
        c_data = {}

        _ex(cause, c_data)

        parent['cause_data'] = c_data

        cause = cause.__cause__
        parent = c_data


def _transfer_valid(d: dict, s: dict, m, excluded_values: list = None):
    if excluded_values is None:
        excluded_values = [None]

    if isinstance(m, dict):
        for key, new_name in m.items():
            # print(f"key = {key}, name = {new_name}, m = {m}, s = {s}")
            if key in s.keys():
                v = s[key]
                # print(f"s[{key}] = {v} for key in {s}")
                if v not in excluded_values:
                    # print(f"d[{new_name}] = {v}")
                    d[new_name] = v
                    # print(f"d = {d}")
    else:
        for key in m:
            if key in s.keys():
                v = s[key]
                if v not in excluded_values:
                    d[key] = v


def _parse_datetime(data: dict, key: str = None) -> datetime:
    if data is None:
        return None

    if key is not None:
        if key in data.keys():
            value = data[key]

            if print_debug: print(f"value = {value}")

            parsed_date = None

            try:
                parsed_date = timezone.datetime.fromisoformat(value).replace(tzinfo=timezone.utc)
            except:
                parsed_date = None

            if parsed_date is not None:
                return parsed_date

            try:
                parsed_date = timezone.datetime.combine(date.fromisoformat(value),
                                                        time(hour=0, minute=0, second=0)).replace(tzinfo=timezone.utc)
            except:
                parsed_date = None

            if parsed_date is not None:
                return parsed_date

            try:
                parsed_date = timezone.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
            except:
                parsed_date = None

            if parsed_date is not None:
                return parsed_date

            try:
                parsed_date = timezone.datetime.fromtimestamp(value)
            except:
                parsed_date = None

            if parsed_date is not None:
                return parsed_date

            raise ValueError(f"Could not parse {value} as a date or time")

        else:
            return None

    else:
        keys = ['year', 'month', 'day', 'hour', 'minute', 'second']

        values = {}

        for key in keys:
            try:
                values[key] = int(data[key]) if key in data else 0
            except:
                values[key] = 0

        return timezone.datetime(**values)


# Primary
class ProfileRetrievalViewSet(viewsets.ModelViewSet):
    #queryset = Profile.objects.all()
    serializer_class = ProfileRetrievalSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    @action(detail=False, methods=['GET', 'POST'], url_path='user')
    def user(self, request, *arg, **kwargs):
        if print_debug or print_debug2: print(f"Profile request received for user")
        if print_debug: print(request)
        if print_debug: print(dir(request))

        try:
            user: User = request.user

            if print_debug: print(user)

            serializer = ProfileRetrievalSerializer(user.profile, many=False)

            #response = {'message': 'Profile Found', 'result': serializer.data}

            to_send = Response(serializer.data, status=status.HTTP_200_OK)
            if print_debug or print_debug2: print(to_send)
            return to_send
        except Exception as e:
            if print_debug or print_debug2: print(e)
            return Response(_m(f"Could not access profile ({e})"), status=status.HTTP_400_BAD_REQUEST)


class DataPointRetrievalViewSet(viewsets.ModelViewSet):
    serializer_class = DataPointSerializerDisplay
    permission_classes = (IsAuthenticated,)

    _point_data_type = None
    _point_origin = None

    class Meta:
        abstract = True

    def _qs(self, user: User, join=False, *args, **kwargs):
        q: QuerySet
        qs: list

        if print_debug: print(f"DataPointRetrievalViewSet._qs({user}, {join}, {kwargs})")

        if self._point_data_type == Indicator.DataType.INT.value:
            qs = [IntDataPoint.objects.filter(user=user, **kwargs)]
        elif self._point_data_type == Indicator.DataType.FLOAT.value:
            qs = [FloatDataPoint.objects.filter(user=user, **kwargs)]
        else:
            qs = [IntDataPoint.objects.filter(user=user, **kwargs), FloatDataPoint.objects.filter(user=user, **kwargs)]

        if self._point_origin is not None:
            new_qs = []
            for q in qs:
                new_qs.append(q.filter(indicator__origin=self._point_origin))
            qs = new_qs

        if join:
            q = qs[0]
            if len(qs) > 1:
                q = q.union(qs[1])
            return q
        return qs

    def get_queryset(self):
        user: User = self.request.user

        return self._qs(user=user, join=True).order_by('-time')

    @action(detail=False, methods=['GET', 'POST'], url_path='user')
    def all(self, request, *arg, **kwargs):
        try:
            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            max_values = 100
            if data is not None and 'max_values' in data.keys():
                if print_debug: print(f"data['max_values'] = {data['max_values']}")
                max_values = data['max_values']

            ad_kwargs = {}

            min_date: datetime = _parse_datetime(data, 'min_date')
            if min_date is not None:
                ad_kwargs['time__gte'] = min_date

            max_date: datetime = _parse_datetime(data, 'max_date')
            if max_date is not None:
                ad_kwargs['time__lte'] = max_date

            q: QuerySet = self._qs(user=user, join=True, **ad_kwargs).order_by('-time')

            points: QuerySet = None
            if max_values is not None:
                points = q[:max_values]
            else:
                points = q.all()

            serializer = DataPointSerializerDisplay(points, many=True)

            to_send = Response(serializer.data, status=status.HTTP_200_OK)
            # to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)

            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET', 'POST'], url_path='user')
    def single(self, request, pk=None, *arg, **kwargs):
        try:
            if pk is None:
                return _bad("No key provided.")

            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            max_values = None
            if data is not None and 'max_values' in data.keys():
                if print_debug: print(f"data['max_values'] = {data['max_values']}")
                max_values = data['max_values']

            indicator: Indicator = Indicator.objects.prefetch_related('int_data_points', 'float_data_points').get(pk=pk)

            q: QuerySet = indicator.data_class().objects.filter(user=user, indicator=indicator)

            min_date: datetime = _parse_datetime(data, 'min_date')
            if min_date is not None:
                q = q.filter(time__gte=min_date)

            max_date: datetime = _parse_datetime(data, 'max_date')
            if max_date is not None:
                q = q.filter(time__lte=max_date)

            q = q.order_by('-time')

            points: QuerySet = None
            if max_values is not None:
                points = q[:max_values]
            else:
                points = q.all()

            serializer = DataPointSerializerDisplay(points, many=True)

            to_send = Response(serializer.data, status=status.HTTP_200_OK)
            # to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)

            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def _submit(self, request, pk=None):
        if print_debug or print_debug2: print(f"Submission received for form #{pk}")
        if print_debug: print(request)
        if print_debug: print(dir(request))
        if print_debug: print(request.data)
        # SurveyViewSetFrontEnd.last_request = request
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")
            if pk is None:
                return _bad("No key provided.")

            # Validate

            # Check for replacement

            if print_debug: print("check 1")

            user = request.user  # TODO

            if print_debug: print(user)

            form = Form.objects.get(id=pk)
            if print_debug: print(form)

            submission_data = request.data
            if print_debug or print_debug2: print(
                f"submission_data = {submission_data} \n... {dict(submission_data)}")
            if print_debug: print(type(submission_data))

            if 'time' in dir(request):
                time = request.data['time']
            elif 'time' in submission_data:
                time = submission_data['time']
            else:
                time = timezone.now()  # Django set to utc
                # datetime.utcnow().replace(tzinfo=timezone.utc)  #
            if print_debug: print(time)

            if isinstance(submission_data, dict):
                raw_data = json.dumps(submission_data)
                if print_debug or print_debug2: print(f"dict -> raw_data = {raw_data}")
            elif isinstance(submission_data, str):
                raw_data = submission_data
                if print_debug or print_debug2: print(f"str -> raw_data = {raw_data}")
            else:
                raw_data = submission_data
                if print_debug or print_debug2: print(f"? -> raw_data = {raw_data}")

            submission = Submission.objects.create(user=user, form=form, time=time, raw_data=raw_data)
            if print_debug: print(submission)

            try:
                if print_debug or print_debug2: print('check 2')
                submission.process(submission.r_validate())
                if print_debug or print_debug2: print('check 3')
            except ValidationError as e:
                if print_debug or print_debug2: print(f"Validation: {e}")

                try:
                    if hasattr(e, 'rev_error_list') and \
                            hasattr(e, 'rev_error_nums') and \
                            hasattr(e, 'rev_error_elements'):
                        errors = []
                        errors_flat = []

                        for error, n, group in zip(e.rev_error_list, e.rev_error_nums, e.rev_error_elements):
                            # print(f"error = {error}, n = {n}, group = {group}")
                            e_data = {
                                    'position_in_form': n,
                                    'group_data'      : group
                            }

                            _recursive_exception_parse(error, e_data)

                            if hasattr(error, 'rev_error_list') and \
                                    hasattr(error, 'rev_error_nums') and \
                                    hasattr(error, 'rev_error_questions'):
                                q_errors = []
                                for q_error, q_n, question in zip(error.rev_error_list,
                                                                  error.rev_error_nums,
                                                                  error.rev_error_questions):
                                    # print(f"q_error = {q_error}, q_n = {q_n}, question = {question}")
                                    question: dict
                                    qe_data = {
                                            'position_in_form'   : n,
                                            'group_data'         : group,
                                            'position_in_element': q_n,
                                            'question_data'      : question
                                    }

                                    _recursive_exception_parse(q_error, qe_data)

                                    _transfer_valid(qe_data, question, {'number': 'question_number'})
                                    _transfer_valid(qe_data, question, ['id', 'response'])
                                    _transfer_valid(qe_data, group, {'number': 'group_number', 'id': 'group_id'})
                                    _transfer_valid(qe_data, group, ['element_type',
                                                                     'question_group_type',
                                                                     'question_group_type_data'])

                                    q_errors.append(qe_data)
                                    errors_flat.append(qe_data)

                                if len(q_errors) > 0: e_data['questions'] = q_errors

                            errors.append(e_data)

                        response = {
                                'message': _("Submission could not be validated."),
                                'errors' : errors_flat
                        }
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                except Exception as ex:
                    # print(ex) # TODO
                    pass

                return _r(f"Could not validate submission ({e})", status.HTTP_400_BAD_REQUEST)

            # acs: 'QuerySet' = user.profile.all_completed_surveys()
            # for sub in acs:
            #     print(SubmissionSerializer(sub, many=False).data)

            serializer = SubmissionSerializer(submission, many=False)

            response = {'message': 'Submission received', 'result': serializer.data}

            if print_debug: print(f"status.HTTP_201_CREATED = {status.HTTP_201_CREATED}")
            to_send = Response(response, status=status.HTTP_201_CREATED)
            if print_debug or print_debug2: print(to_send)
            return to_send
        except Exception as e:
            if print_debug or print_debug2: print(e)
            return _r(f"Could not parse submission ({e})", status.HTTP_400_BAD_REQUEST)

    #@action(detail=True, methods=['POST', 'GET'])
    def _retrieve(self, request, pk=None, *args, **kwargs):
        set: QuerySet = Form.objects.filter(type=Form.FormType.SURVEY.value)
        form: Form = set.get(pk=pk)

        serializer = FormSerializerDisplay(form, many=False)

        to_send = Response(serializer.data, status=status.HTTP_200_OK)
        # to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)

        if print_debug: print(to_send)
        return to_send


class LabValueRetrievalViewSet(DataPointRetrievalViewSet):
    _point_origin = Indicator.OriginType.LAB.value


class SurveyValueRetrievalViewSet(DataPointRetrievalViewSet):
    _point_origin = Indicator.OriginType.SURVEY.value


class IndicatorRetrievalViewSet(viewsets.ModelViewSet):
    _model = Indicator
    serializer_class = IndicatorSerializer
    permission_classes = (IsAuthenticated,)

    _point_origin = None

    def _qs(self, user: User, join=False, to_type: dict = {}, *args, **kwargs):
        q: QuerySet
        qs: list

        if print_debug: print(f"IndicatorRetrievalViewSet._qs({user}, {join}, {to_type}, {kwargs})")

        i_kwargs = {}
        f_kwargs = {}

        for k, v in to_type.items():
            i_kwargs[f"int_data_points__{k}"] = v
            f_kwargs[f"float_data_points__{k}"] = v

        if print_debug: print(f"IndicatorRetrievalViewSet._qs : {i_kwargs};\t{f_kwargs}")

        qs = [Indicator.objects.filter(int_data_points__user=user, **i_kwargs, **kwargs),
              Indicator.objects.filter(float_data_points__user=user, **f_kwargs, **kwargs)]

        new_qs = []
        for q in qs:
            if self._point_origin is not None:
                new_qs.append(q.filter(origin=self._point_origin).distinct())
            else:
                new_qs.append(q.distinct())
        qs = new_qs

        if join:
            q = qs[0]
            if len(qs) > 1:
                q = q.union(qs[1])
            return q
        return qs

    def get_queryset(self):
        user: User = self.request.user

        q: QuerySet
        qs: list = self._qs(user=user)

        q = qs[0]
        if len(qs) > 1:
            q = q.union(qs[1])

        return q

    @action(detail=False, methods=['GET', 'POST'], url_path='user')
    def all(self, request, *arg, **kwargs):
        try:
            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            max_values = 100
            if data is not None and 'max_values' in data.keys():
                if print_debug: print(f"data['max_values'] = {data['max_values']}")
                max_values = data['max_values']

            ad_kwargs = {}

            min_date: datetime = _parse_datetime(data, 'min_date')
            if min_date is not None:
                ad_kwargs['time__gte'] = min_date

            max_date: datetime = _parse_datetime(data, 'max_date')
            if max_date is not None:
                ad_kwargs['time__lte'] = max_date

            q: QuerySet = self._qs(user=user, join=True, to_type=ad_kwargs)

            indicators: QuerySet = None
            if max_values is not None:
                indicators = q[:max_values]
            else:
                indicators = q.all()

            serializer = IndicatorSerializer(indicators, many=True)

            to_send = Response(serializer.data, status=status.HTTP_200_OK)
            # to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)

            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET', 'POST'], url_path='user/recent')
    def recent(self, request, pk=None, *arg, **kwargs):
        if print_debug: print(f"Filtered indicator data request received for user")
        try:
            user: User = request.user

            if print_debug: print(user)

            indicator: Indicator = Indicator.objects.prefetch_related('int_data_points', 'float_data_points').get(pk=pk)

            point = indicator.data_class().objects.filter(user=user).latest('time')

            serializer = DataPointSerializerDisplay(point, many=False)

            to_send = Response(serializer.data, status=status.HTTP_200_OK)
            # to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)

            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)


class SurveyIndicatorRetrievalViewSet(IndicatorRetrievalViewSet):
    _point_origin = Indicator.OriginType.SURVEY.value


class LabIndicatorRetrievalViewSet(IndicatorRetrievalViewSet):
    _point_origin = Indicator.OriginType.LAB.value


class SurveyViewSetFrontEnd(viewsets.ModelViewSet):
    _model = Form
    serializer_class = FormSerializerDisplay
    queryset = _model.objects.filter(type=Form.FormType.SURVEY.value)
    permission_classes = (IsAuthenticated,)

    # def get_queryset(self):
    #     return Form.objects.filter(type=Form.FormType.SURVEY.value)

    @action(detail=True, methods=['POST'])
    def submit(self, request, pk=None):
        if print_debug or print_debug2: print(f"Submission received for form #{pk}")
        if print_debug: print(request)
        if print_debug: print(dir(request))
        if print_debug: print(request.data)
        #SurveyViewSetFrontEnd.last_request = request
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")
            if pk is None:
                return _bad("No key provided.")

            # Validate

            # Check for replacement

            if print_debug: print("check 1")

            user = request.user  # TODO

            if print_debug: print(user)

            form = Form.objects.get(id=pk)
            if print_debug: print(form)

            submission_data = request.data
            if print_debug or print_debug2: print(f"submission_data = {submission_data} \n... {dict(submission_data)}")
            if print_debug: print(type(submission_data))

            if 'time' in dir(request):
                time = request.data['time']
            elif 'time' in submission_data:
                time = submission_data['time']
            else:
                time = timezone.now() # Django set to utc
                # datetime.utcnow().replace(tzinfo=timezone.utc)  #
            if print_debug: print(time)

            if isinstance(submission_data, dict):
                raw_data = json.dumps(submission_data)
                if print_debug or print_debug2: print(f"dict -> raw_data = {raw_data}")
            elif isinstance(submission_data, str):
                raw_data = submission_data
                if print_debug or print_debug2: print(f"str -> raw_data = {raw_data}")
            else:
                raw_data = submission_data
                if print_debug or print_debug2: print(f"? -> raw_data = {raw_data}")

            submission = Submission.objects.create(user=user, form=form, time=time, raw_data=raw_data)
            if print_debug: print(submission)

            try:
                if print_debug or print_debug2: print('check 2')
                submission.process(submission.r_validate())
                if print_debug or print_debug2: print('check 3')
            except ValidationError as e:
                if print_debug or print_debug2: print(f"Validation: {e}")

                try:
                    if hasattr(e, 'rev_error_list') and \
                            hasattr(e, 'rev_error_nums') and \
                            hasattr(e, 'rev_error_elements'):
                        errors = []
                        errors_flat = []

                        for error, n, group in zip(e.rev_error_list, e.rev_error_nums, e.rev_error_elements):
                            # print(f"error = {error}, n = {n}, group = {group}")
                            e_data = {
                                    'position_in_form' : n,
                                    'group_data' : group
                                           }

                            _recursive_exception_parse(error, e_data)

                            if hasattr(error, 'rev_error_list') and \
                                    hasattr(error, 'rev_error_nums') and \
                                    hasattr(error, 'rev_error_questions'):
                                q_errors = []
                                for q_error, q_n, question in zip(error.rev_error_list,
                                                                  error.rev_error_nums,
                                                                  error.rev_error_questions):
                                    # print(f"q_error = {q_error}, q_n = {q_n}, question = {question}")
                                    question: dict
                                    qe_data = {
                                            'position_in_form' : n,
                                            'group_data' : group,
                                            'position_in_element' : q_n,
                                            'question_data' : question
                                                   }

                                    _recursive_exception_parse(q_error, qe_data)

                                    _transfer_valid(qe_data, question, {'number': 'question_number'})
                                    _transfer_valid(qe_data, question, ['id', 'response'])
                                    _transfer_valid(qe_data, group, {'number': 'group_number', 'id': 'group_id'})
                                    _transfer_valid(qe_data, group, ['element_type',
                                                                     'question_group_type',
                                                                     'question_group_type_data'])

                                    q_errors.append(qe_data)
                                    errors_flat.append(qe_data)

                                if len(q_errors) > 0: e_data['questions'] = q_errors

                            errors.append(e_data)

                        response = {
                                'message' : _("Submission could not be validated."),
                                'errors' : errors_flat
                                    }
                        return Response(response, status=status.HTTP_400_BAD_REQUEST)
                except Exception as ex:
                    # print(ex) # TODO
                    pass

                return _r(f"Could not validate submission ({e})", status.HTTP_400_BAD_REQUEST)

            # acs: 'QuerySet' = user.profile.all_completed_surveys()
            # for sub in acs:
            #     print(SubmissionSerializer(sub, many=False).data)

            serializer = SubmissionSerializer(submission, many=False)

            response = {'message': 'Submission received', 'result': serializer.data}

            if print_debug: print(f"status.HTTP_201_CREATED = {status.HTTP_201_CREATED}")
            to_send = Response(response, status=status.HTTP_201_CREATED)
            if print_debug or print_debug2: print(to_send)
            return to_send
        except Exception as e:
            if print_debug or print_debug2: print(e)
            return _r(f"Could not parse submission ({e})", status.HTTP_400_BAD_REQUEST)


class UserSurveyHistoryViewSet(viewsets.ModelViewSet):
    _model = Submission
    serializer_class = UserSubmissionHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        #profile: Profile = self.request.user.profile
        return Submission.objects.filter(user=self.request.user, form__type=Form.FormType.SURVEY.value, processed=True)

    @action(detail=False, methods=['GET', 'POST'])
    def available(self, request, *args, **kwargs):
        try:
            user: User = request.user

            serializer = AvailableSurveySerializer(user.get_available_surveys(), many=True)

            to_send = Response(serializer.data, status=status.HTTP_201_CREATED)
            if print_debug or print_debug2: print(to_send)
            return to_send
        except Exception as e:
            if print_debug or print_debug2: print(e)
            return _r(f"Could not find surveys ({e})", status.HTTP_400_BAD_REQUEST)

    #@action(detail=True, methods=['POST', 'GET'])
    def _retrieve(self, request, pk=None, *args, **kwargs):
        set: QuerySet = Form.objects.filter(type=Form.FormType.SURVEY.value)
        form: Form = set.get(pk=pk)

        serializer = FormSerializerDisplay(form, many=False)

        to_send = Response(serializer.data, status=status.HTTP_200_OK)
        # to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)

        if print_debug: print(to_send)
        return to_send


class AvailableSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = AvailableSurveySerializer


class UserIndicatorDataViewSet(viewsets.ModelViewSet):
    _model = Indicator
    serializer_class = UserIndicatorDataSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # , origin=Indicator.OriginType.SURVEY.value
        user: User = self.request.user
        return Indicator.objects.filter(float_data_points__user=user).distinct()\
            .all().union(Indicator.objects.filter(int_data_points__user=user)
                         .distinct().all())


class UserIndicatorViewSet(viewsets.ModelViewSet):
    _model = Indicator
    serializer_class = IndicatorSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user: User = self.request.user
        return Indicator.objects.filter(float_data_points__user=user).distinct()\
            .all().union(Indicator.objects.filter(int_data_points__user=user)
                         .distinct().all())

    @action(detail=True, methods=['GET'])
    def data(self, request, pk=None, *arg, **kwargs):
        if print_debug: print(f"Indicator data request received for user")
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")
            if pk is None:
                return _bad("No key provided.")

            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            indicator: Indicator = Indicator.objects.get(pk=pk)

            points: QuerySet = None

            # if indicator.is_int():
            #     points = IntDataPoint.objects.filter(user=user)
            # elif indicator.is_float():
            #     points = FloatDataPoint.objects.filter(user=user)

            max_values = 100
            if 'max_values' in data.keys():
                if print_debug: print(f"data['max_values'] = {data['max_values']}")
                max_values = data['max_values']

            if 'min_date' in data.keys():
                if 'max_date' in data.keys():
                    if print_debug: print(f"data['min_date'] = {data['min_date']}, data['max_date'] = {data['max_date']}")
                    points = indicator.data_class().objects.filter(user=user,
                                                                   time__gte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['min_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   time__lte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['max_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   indicator=indicator
                                                                   ).order_by('-time').all()
                else:
                    if print_debug: print(f"data['min_date'] = {data['min_date']}")
                    points = indicator.data_class().objects.filter(user=user,
                                                                   time__gte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['min_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   indicator=indicator
                                                                   ).order_by('-time')[:max_values]
            elif 'max_date' in data.keys():
                if print_debug: print(f"data['max_date'] = {data['max_date']}")
                points = indicator.data_class().objects.filter(user=user,
                                                               time__lte=timezone.datetime.combine(date
                                                                   .fromisoformat(
                                                                       data['max_date']),
                                                                       time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                               indicator=indicator
                                                               ).order_by('-time')[:max_values]
            else:
                if print_debug: print(f"data has no date range")
                points = indicator.data_class().objects.filter(user=user,
                                                               indicator=indicator).order_by('-time')[:max_values]

            if points is not None: # TODO length check?
                if print_debug: print(f"points is not none")
                serializer = DataPointSerializerDisplayBasic(points, many=True)

                response = {'message': 'Data Found',
                            'indicator_data': indicator.get_graph_info(user=user),
                            'data_points': serializer.data}

                if print_debug: print(f"|points| = {len(points)}")

                to_send = Response(response, status=status.HTTP_200_OK)
            else:
                to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)
            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def all_data(self, request, *arg, **kwargs):
        if print_debug: print(f"Indicator data request received for user")
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")

            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            max_values = 100
            if 'max_values' in data.keys():
                if print_debug: print(f"data['max_values'] = {data['max_values']}")
                max_values = data['max_values']

            min_date: datetime = _parse_datetime(data, 'min_date')
            max_date: datetime = _parse_datetime(data, 'max_date')

            indicators: QuerySet = Indicator.objects.filter(float_data_points__user=user).distinct().all()\
                .union(Indicator.objects.filter(int_data_points__user=user).distinct().all())

            indicator: Indicator

            indicator_data = []

            for indicator in indicators:
                points: QuerySet = None

                if min_date is not None:
                    if max_date is not None:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time').all()
                    else:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time')[:max_values]
                elif max_date is not None:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time')[:max_values]
                else:
                    points = indicator.data_class().objects.filter(user=user,
                                                                   indicator=indicator).order_by('-time')[:max_values]

                if points is not None:
                    serializer = DataPointSerializerDisplayBasic(points, many=True)

                    indicator_data.append({'indicator_data': indicator.get_graph_info(user=user),
                                           'data_points': serializer.data})

            if len(indicator_data) > 0:
                response = {'message': 'Data Found',
                            'all_indicator_data': indicator_data}

                to_send = Response(response, status=status.HTTP_200_OK)
            else:
                to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)
            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)


class UserSurveyIndicatorViewSet(viewsets.ModelViewSet):
    _model = Indicator
    serializer_class = IndicatorSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user: User = self.request.user
        return Indicator.objects.filter(float_data_points__user=user, origin=Indicator.OriginType.SURVEY.value)\
            .distinct().all().union(
                Indicator.objects.filter(int_data_points__user=user, origin=Indicator.OriginType.SURVEY.value)
                         .distinct().all())

    @action(detail=True, methods=['GET'])
    def data(self, request, pk=None, *arg, **kwargs):
        if print_debug: print(f"Indicator data request received for user")
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")
            if pk is None:
                return _bad("No key provided.")

            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            indicator: Indicator = Indicator.objects.get(pk=pk)

            points: QuerySet = None

            # if indicator.is_int():
            #     points = IntDataPoint.objects.filter(user=user)
            # elif indicator.is_float():
            #     points = FloatDataPoint.objects.filter(user=user)

            max_values = 100
            if 'max_values' in data.keys():
                if print_debug: print(f"data['max_values'] = {data['max_values']}")
                max_values = data['max_values']

            if 'min_date' in data.keys():
                if 'max_date' in data.keys():
                    if print_debug: print(f"data['min_date'] = {data['min_date']}, data['max_date'] = {data['max_date']}")
                    points = indicator.data_class().objects.filter(user=user,
                                                                   time__gte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['min_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   time__lte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['max_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   indicator=indicator
                                                                   ).order_by('-time').all()
                else:
                    if print_debug: print(f"data['min_date'] = {data['min_date']}")
                    points = indicator.data_class().objects.filter(user=user,
                                                                   time__gte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['min_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   indicator=indicator
                                                                   ).order_by('-time')[:max_values]
            elif 'max_date' in data.keys():
                if print_debug: print(f"data['max_date'] = {data['max_date']}")
                points = indicator.data_class().objects.filter(user=user,
                                                               time__lte=timezone.datetime.combine(date
                                                                   .fromisoformat(
                                                                       data['max_date']),
                                                                       time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                               indicator=indicator
                                                               ).order_by('-time')[:max_values]
            else:
                if print_debug: print(f"data has no date range")
                points = indicator.data_class().objects.filter(user=user,
                                                               indicator=indicator).order_by('-time')[:max_values]

            if points is not None: # TODO length check?
                if print_debug: print(f"points is not none")
                serializer = DataPointSerializerDisplayBasic(points, many=True)

                response = {'message': 'Data Found',
                            'indicator_data': indicator.get_graph_info(user=user),
                            'data_points': serializer.data}

                if print_debug: print(f"|points| = {len(points)}")

                to_send = Response(response, status=status.HTTP_200_OK)
            else:
                to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)
            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def all_data(self, request, *arg, **kwargs):
        if print_debug: print(f"Indicator data request received for user")
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")

            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            max_values = 100
            if 'max_values' in data.keys():
                if print_debug: print(f"data['max_values'] = {data['max_values']}")
                max_values = data['max_values']

            min_date: datetime = _parse_datetime(data, 'min_date')
            max_date: datetime = _parse_datetime(data, 'max_date')

            indicators: QuerySet = Indicator.objects.filter(float_data_points__user=user, origin=Indicator.OriginType.SURVEY.value).distinct().all()\
                .union(Indicator.objects.filter(int_data_points__user=user, origin=Indicator.OriginType.SURVEY.value).distinct().all())

            indicator: Indicator

            indicator_data = []

            for indicator in indicators:
                points: QuerySet = None

                if min_date is not None:
                    if max_date is not None:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time').all()
                    else:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time')[:max_values]
                elif max_date is not None:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time')[:max_values]
                else:
                    points = indicator.data_class().objects.filter(user=user,
                                                                   indicator=indicator).order_by('-time')[:max_values]

                if points is not None:
                    serializer = DataPointSerializerDisplayBasic(points, many=True)

                    indicator_data.append({'indicator_data': indicator.get_graph_info(user=user),
                                           'data_points': serializer.data})

            if len(indicator_data) > 0:
                response = {'message': 'Data Found',
                            'all_indicator_data': indicator_data}

                to_send = Response(response, status=status.HTTP_200_OK)
            else:
                to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)
            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)


class UserLabIndicatorViewSet(viewsets.ModelViewSet):
    # _model = FloatDataPoint
    # serializer_class = FloatDataPointSerializer
    # queryset = _model.objects.all()
    _model = Indicator
    serializer_class = IndicatorSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user: User = self.request.user
        return Indicator.objects.filter(float_data_points__user=user, origin=Indicator.OriginType.LAB.value).distinct()\
            .all().union(Indicator.objects.filter(int_data_points__user=user, origin=Indicator.OriginType.LAB.value)\
                         .distinct().all())

    @action(detail=True, methods=['GET'])
    def data(self, request, pk=None, *arg, **kwargs):
        if print_debug: print(f"Indicator data request received for user")
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")
            if pk is None:
                return _bad("No key provided.")

            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            indicator: Indicator = Indicator.objects.get(pk=pk)

            points: QuerySet = None

            # if indicator.is_int():
            #     points = IntDataPoint.objects.filter(user=user)
            # elif indicator.is_float():
            #     points = FloatDataPoint.objects.filter(user=user)

            max_values = 100
            if 'max_values' in data.keys():
                max_values = data['max_values']

            #print(data.keys())

            if 'min_date' in data.keys():
                if 'max_date' in data.keys():
                    points = indicator.data_class().objects.filter(user=user,
                                                                   time__gte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['min_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   time__lte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['max_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   indicator=indicator
                                                                   ).order_by('-time').all()
                else:
                    points = indicator.data_class().objects.filter(user=user,
                                                                   time__gte=timezone.datetime.combine(date
                                                                       .fromisoformat(
                                                                           data['min_date']),
                                                                           time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                                   indicator=indicator
                                                                   ).order_by('-time')[:max_values]
            elif 'max_date' in data.keys():
                points = indicator.data_class().objects.filter(user=user,
                                                               time__lte=timezone.datetime.combine(date
                                                                   .fromisoformat(
                                                                       data['max_date']),
                                                                       time(hour=0, minute=0, second=0))
                                                               .replace(tzinfo=timezone.utc),
                                                               indicator=indicator
                                                               ).order_by('-time')[:max_values]
            else:
                points = indicator.data_class().objects.filter(user=user,
                                                               indicator=indicator).order_by('-time')[:max_values]

            if points is not None: # TODO length check?
                serializer = DataPointSerializerDisplayBasic(points, many=True)

                response = {'message': 'Data Found',
                            'indicator_data': indicator.get_graph_info(user=user),
                            'data_points': serializer.data}

                to_send = Response(response, status=status.HTTP_200_OK)
            else:
                to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)
            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['GET'])
    def all_data(self, request, *arg, **kwargs):
        if print_debug: print(f"Indicator data request received for user")
        try:
            if 'data' not in dir(request):
                return _bad("Must provide submission data.")

            user: User = request.user
            data: dict = request.data

            if print_debug: print(user)

            max_values = 100
            if 'max_values' in data.keys():
                if print_debug: print(f"data['max_values'] = {data['max_values']}")
                max_values = data['max_values']

            min_date: datetime = _parse_datetime(data, 'min_date')
            max_date: datetime = _parse_datetime(data, 'max_date')

            indicators: QuerySet = Indicator.objects.filter(float_data_points__user=user, origin=Indicator.OriginType.LAB.value).distinct().all()\
                .union(Indicator.objects.filter(int_data_points__user=user, origin=Indicator.OriginType.LAB.value).distinct().all())

            indicator: Indicator

            indicator_data = []

            for indicator in indicators:
                points: QuerySet = None

                if min_date is not None:
                    if max_date is not None:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time').all()
                    else:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time')[:max_values]
                elif max_date is not None:
                        points = indicator.data_class().objects.filter(user=user,
                                                                       time__gte=min_date, time__lte=max_date,
                                                                       indicator=indicator
                                                                       ).order_by('-time')[:max_values]
                else:
                    points = indicator.data_class().objects.filter(user=user,
                                                                   indicator=indicator).order_by('-time')[:max_values]

                if points is not None:
                    serializer = DataPointSerializerDisplayBasic(points, many=True)

                    indicator_data.append({'indicator_data': indicator.get_graph_info(user=user),
                                           'data_points': serializer.data})

            if len(indicator_data) > 0:
                response = {'message': 'Data Found',
                            'all_indicator_data': indicator_data}

                to_send = Response(response, status=status.HTTP_200_OK)
            else:
                to_send = Response(_m('No Data Found'), status=status.HTTP_200_OK)
            if print_debug: print(to_send)
            return to_send
        except Exception as e:
            if print_debug: print(e)
            return Response(_m(f"Could not access data ({e})"), status=status.HTTP_400_BAD_REQUEST)


class LabValueViewSet(viewsets.ModelViewSet):
    _model = Submission
    serializer_class = UserSubmissionHistorySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # profile: Profile = self.request.user.profile
        return Submission.objects.filter(user=self.request.user, form__type=Form.FormType.MEDICAL_LAB.value, processed=True)
