from django.http import JsonResponse
from django.db import models

from common.serializer import Serializer


class ApiJsonResponse(JsonResponse):
    def __init__(self, data=None, message="success", code=200, httpCode=201, **kwargs):
        if isinstance(data, models.Model):
            data = Serializer(data).serialize(hidden=["password"])

        super().__init__({"message": message, "code": code, "data": data},json_dumps_params={
            "ensure_ascii": False,
            "indent": 4,
            "sort_keys": False,
        })
        self.status_code = httpCode
        self.content_type = "application/json"

    @staticmethod
    def success(data=None, message="success", code=200):
        return ApiJsonResponse(data=data, message=message, code=code, httpCode=200)

    @staticmethod
    def error(data=None, message="error", code=500):
        return ApiJsonResponse(data=data, message=message, code=code, httpCode=500)
