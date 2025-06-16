from rest_framework import routers
from django.urls import path, include
from .views import ProductViewSet, CustomerOrderViewSet

router = routers.DefaultRouter()
router.register("products", ProductViewSet)
router.register("orders", CustomerOrderViewSet)
urlpatterns = router.urls
path("api/", include("orders.urls"))
