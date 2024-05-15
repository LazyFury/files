from django.db import models
from django.http import HttpRequest

from common.response import ApiJsonResponse
from common.router import Router
from common.serializer import Serializer


class Api:
    model: models.Model

    create_fields = []
    update_fields = []
    hidden_fields = ['password']

    def __init__(self, model: models.Model) -> None:
        self.model = model

    def search_condition(self, request: HttpRequest) -> dict:
        return {}

    def get(self, request: HttpRequest) -> ApiJsonResponse:
        id = request.GET.get("id")
        data = self.model.objects.filter(**self.search_condition(request=request)).filter(pk=id).first()
        if not data:
            return ApiJsonResponse.error(message="Not Found", code=404)
        return ApiJsonResponse.success(
            Serializer(data).serialize(hidden=self.hidden_fields)
        )

    def list(self, request: HttpRequest) -> ApiJsonResponse:
        params = request.GET.dict()
        limit = params.pop("limit", 10)
        limit = int(limit)
        page = params.pop("page", 1)
        page = int(page)
        start = (page - 1) * limit
        end = page * limit
        list = (
            self.model.objects.filter(**params)
            .filter(self.search_condition(request=request))
            .all()[start:end]
        )
        return ApiJsonResponse.success([Serializer(item).serialize(hidden=self.hidden_fields) for item in list])

    def create(self, request: HttpRequest) -> ApiJsonResponse:
        data = request.POST.dict()
        for k in data:
            if k not in self.create_fields:
                data.pop(k)
        result = self.model.objects.create(**data)
        return ApiJsonResponse.success(result)

    def update(self, request: HttpRequest) -> ApiJsonResponse:
        id = request.POST.get("id")
        data = request.POST.dict()
        for k in data:
            if k not in self.update_fields:
                data.pop(k)
        result = self.model.objects.filter(id=id).update(**data)
        return ApiJsonResponse.success(result)

    def delete(self, request: HttpRequest) -> ApiJsonResponse:
        id = request.POST.get("id")
        result = self.model.objects.filter(id=id).delete()
        return ApiJsonResponse.success(result)

    def register(self, router: Router, path: str = None):
        print(f"/api/{self.model._meta.model_name}")
        path = path or f"/api/{self.model._meta.model_name}"

        router.get(f"{path}/detail")(self.get)
        router.get(f"{path}/list")(self.list)
        router.post(f"{path}/create")(self.create)
        router.post(f"{path}/update")(self.update)
        router.post(f"{path}/delete")(self.delete)
