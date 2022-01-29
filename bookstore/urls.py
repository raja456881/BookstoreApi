from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register("book/api", BookApiViewSet, basename="bookapi")
router.register("orderapi", OrderApiViewSet, basename="orderapi")
router.register("",  UserApiViewSet, basename="userapi")
urlpatterns = [
    path("", include(router.urls)),
    path("order/list/", OrderSortapiViewSet.as_view(), name="orderlist"),
    path("search/book/",SearchBookNameApiView.as_view(), name="searchBook"),
    path("catergory/book/list", CatergoryListBookApiView.as_view(), name="catergory_list_view"),
    path("most/book/buy", GetMostOrderedBookApiView.as_view(), name="GetMostOrderedBookApiView")
]