from django.urls import path
from . import views

urlpatterns = [
    path("routes", views.RoutesAPIView.as_view(), name="product-routes"),
    path("", views.ProductAPIView.as_view(), name="products"),
    path("<int:id>", views.ProductByIdAPIView.as_view(), name="product_by_id"),
    path("categories", views.CategoryAPIView.as_view(), name="categories"),
    path("categories/<int:id>", views.CategoryByIdAPIView.as_view(), name="category_by_id"),
    path("categories/search", views.CategorySearchAPIView.as_view(), name="category_search"),
    path("brands", views.BrandAPIView.as_view(), name="brands"),
    path("brands/<int:id>", views.BrandByIdAPIView.as_view(), name="brand_by_id"),
    path("wishlist", views.WishListAPIView.as_view(), name="wishlist"),
    path("wishlist/<int:id>", views.WishListByIdAPIView.as_view(), name="wishlist_by_id"),
    path("<int:product_id>/reviews", views.ProductReviewAPIView.as_view(), name="product_review"),
    path(
        "<int:product_id>/reviews/<int:id>",
        views.ProductReviewByIdAPIView.as_view(),
        name="product_review_by_id",
    ),
    path("<int:product_id>/rating", views.ProductRatingAPIView.as_view(), name="product_rating"),
]
