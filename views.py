from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer,UserSerializer
from django.shortcuts import get_object_or_404
import redis
from django.conf import settings
import logging
from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView
# inventory/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
import redis
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item
from redis import Redis, ConnectionError
from django.http import JsonResponse

r = redis.Redis()
r = redis.Redis(host='localhost', port=6379, db=0)

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Item.objects.all()
    

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def retrieve(self, request, pk=None):
        # Check Redis cache first
        try:
        # Example logic to get item from Redis
            cached_item = r.get(f"item_{pk}")
            if cached_item is None:
                return JsonResponse({'error': 'Item not found'}, status=404)
            return JsonResponse(cached_item, safe=False)
        except ConnectionError:
            return JsonResponse({'error': 'Could not connect to Redis.'}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def update(self, request, pk=None):
        try:
            item = self.get_queryset().get(pk=pk)
            serializer = self.get_serializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, pk=None):
        try:
            item = self.get_queryset().get(pk=pk)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Item.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class CustomTokenObtainPairView(TokenObtainPairView):
    # Customize if needed
    pass



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description']

    def validate_name(self, value):
        if Item.objects.filter(name=value).exists():
            raise serializers.ValidationError("Item already exists.")
        return value

    

    