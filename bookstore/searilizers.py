from .models import *
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

class Catergorysearilizers(ModelSerializer):
    class Meta:
        model = Category
        fileds = ['book', "name"]

class UserSearilizer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        return user


class BookSearilizer(ModelSerializer):
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj. category.name


    class Meta:
        model = Book
        fields = ['name', "title", "category_name", "descriptions", "prize"]

class MostBookSearilizer(ModelSerializer):
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, obj):
        return obj. category.name


    class Meta:
        model = Book
        fields = ['name', "title", "category_name", "descriptions", "prize", "book_buy"]




class OrderSearilizer(ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


