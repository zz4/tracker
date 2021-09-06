from rest_framework.exceptions import APIException, _get_error_details


class IssueException(APIException):
    status_code = 400
    default_detail = dict()
    default_code = 'error'

    def __init__(self, status_code=None, extra=None):
        detail = self.default_detail
        code = self.default_code
        if extra is not None:
            for _i in extra:
                detail[_i[0]] = _i[1]
        if status_code is not None:
            self.status_code = status_code
        self.detail = _get_error_details(detail, code)
