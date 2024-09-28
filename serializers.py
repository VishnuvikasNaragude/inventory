from rest_framework import serializers
from .models import Item
# inventory/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User
# inventory/serializers.py
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'




#from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Item

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
