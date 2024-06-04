from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, Menu, Vote

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CreateEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class CreateRestaurantAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_staff=True  # Assign staff status to restaurant admin
        )
        return user

class RestaurantSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'owner']

class MenuSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer(read_only=True)
    total_votes = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = ['id', 'name', 'description', 'restaurant', 'date', 'total_votes']

class VoteSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    menu = MenuSerializer(read_only=True)

    class Meta:
        model = Vote
        fields = ['id', 'user', 'menu', 'date']
