from django.db.models import Q
from django.http import Http404
from .serializers import TableSerializer, Currencies_Serializer
from .models import Currency_table, Currencies
from .utils import update_data
import sqlite3

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create your views here.
class TableData(APIView):
    def get(self, request, format=None):
        update_data("Currencies")
        cur_data = Currency_table.objects.all()
        serializer = TableSerializer(cur_data, many=True)

        return Response(serializer.data)


class ProductData(APIView):
    def get(self, request, format=None):
        cur_data = Currencies.objects.all().order_by("date")
        serializer = Currencies_Serializer(cur_data, many=True)

        return Response(serializer.data)
