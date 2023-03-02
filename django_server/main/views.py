from adrf.views import APIView
from asgiref.sync import sync_to_async
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from main.models import Entity


class SimpleView(APIView):
    async def get(self, request):
        return Response({"message": "This is an async class based view."})

    async def post(self, request):
        return Response(request.POST)


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ['id', 'field1', 'field2']


class DBViews(APIView):
    async def get(self, request, f1):
        res = await sync_to_async(Entity.objects.filter(field1=f1).all)()
        ser = EntitySerializer(res, many=True)
        data = await sync_to_async(lambda: ser.data)()
        r = Response(data)
        return r

    async def post(self, request):
        data = JSONParser().parse(request)
        serializer = EntitySerializer(data=data)
        if serializer.is_valid():
            await sync_to_async(serializer.save)()
            return JsonResponse(await sync_to_async(lambda: serializer.data)(), status=201)
        return JsonResponse(serializer.errors, status=400)
