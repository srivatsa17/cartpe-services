from django.urls import path
from . import views

urlpatterns = [
    path('routes', views.RoutesAPIView.as_view(), name="product-routes"),
    path('', views.ProductAPIView.as_view(), name="products"),
    path('<int:id>', views.ProductByIdAPIView.as_view(), name="product_by_id"),
    path('categories', views.CategoryAPIView.as_view(), name="categories"),
    path('categories/<int:id>', views.CategoryByIdAPIView.as_view(), name="category_by_id"),
    path('brands', views.BrandAPIView.as_view(), name="brands"),
    path('brands/<int:id>', views.BrandByIdAPIView.as_view(), name="brand_by_id"),
    path('images', views.ProductImageAPIView.as_view(), name="images"),
    path('images/<int:id>', views.ProductImageByIdAPIView.as_view(), name="image_by_id"),
]