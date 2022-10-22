from django.shortcuts import render
from django.db.models import Q
from django.http import Http404
from .serializers import DocumentSerializer
from .models import Document
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser,JSONParser

class upload_file(APIView):
    parser_classes = [MultiPartParser,JSONParser]
    def put(self, request, format=None):
        print(request.data)
        file_serializer = DocumentSerializer(data=request.FILES)
        if file_serializer.is_valid():
            file_serializer.save()

            return Response(file_serializer.data,
                status=201)
        else:
            print(file_serializer.errors)
            return Response(file_serializer.errors,
                status=400)

    def get(self,request,format=None):
        pdf = Document.objects.all()[0]
        serializer = DocumentSerializer(pdf)

        return Response(serializer.data)