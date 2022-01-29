from .searilizers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Max


class UserApiViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSearilizer


class BookApiViewSet(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSearilizer


class OrderApiViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSearilizer


class OrderSortapiViewSet(APIView):
    def get(self, request, *args, **kwargs):
        try:
            ordersort = Order.objects.all().order_by("time")
            serializers = OrderSearilizer(ordersort, many=True)
            return Response(serializers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)


class SearchBookNameApiView(APIView):
    def get(self, request):
        try:
            name = request.data.get("name")
            if name is not None:
                book = Book.objects.all().filter(name=name)
                booksearilizers = BookSearilizer(book, many=True)
                return Response(booksearilizers.data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Please enter the name"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e))


class CatergoryListBookApiView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            categoty_name: object = request.data.get("categoty")
            if categoty_name is not None:
                book = Book.objects.filter(category__name__iexact=categoty_name).all()
                serializers = BookSearilizer(book, many=True)
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response({"error": "Must have category  name"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(str(e))


class GetMostOrderedBookApiView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            book = Book.objects.all().annotate(sum_of_buy_book=Max("book_buy"))
            searilizers = MostBookSearilizer(book, many=True)
            return Response(searilizers.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e))
