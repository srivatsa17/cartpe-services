from django.urls import path
from . import views

urlpatterns = [
    path('routes', views.RoutesAPIView.as_view(), name="routes"),
    path('', views.ProductAPIView.as_view(), name="products"),
    path('<int:id>', views.ProductByIdAPIView.as_view(), name="product_by_id")
]