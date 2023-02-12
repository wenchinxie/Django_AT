from rest_framework import serializers
from .models import Currency_table, Currencies


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency_table
        fields = ("product", "date", "price", "day", "week", "month", "quarter", "year")


class Currencies_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Currencies
        fields = ("date", "product", "price")
