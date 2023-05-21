from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .serializers import TableSerializer, Currencies_Serializer
from .models import Currency_table, Currencies
from .utils import update_data, merge_dates_with_missing_dates
from Financial_data_crawler.db.ChipModels import Day_Transaction_Info
from Financial_data_crawler.db.ChipModels import Broker_Transaction


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


class DayTransaction(APIView):
    def get(self, request, stockid, format=None):
        day_trans = (
            Day_Transaction_Info.objects(StockID=stockid).order_by("Date").as_pymongo()
        )
        day_trans_data = merge_dates_with_missing_dates(day_trans)
        day_trans_data.pop("_id", None)
        return Response(day_trans_data)


class SelBroker(APIView):
    def get(self, request, stockid, format=None):
        if not (stockid.startswith("0") or len(stockid) > 4):
            revised_id = "AS" + stockid

        broker_trans = (
            Broker_Transaction.objects(stockid=revised_id).order_by("Date").as_pymongo()
        )
        broker_trans_data = merge_dates_with_missing_dates(broker_trans)
        return Response(broker_trans_data)
