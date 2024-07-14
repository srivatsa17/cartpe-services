from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from product_service.routes import routes
from product_service.serializers import (
    ProductSerializer,
    CategorySerializer,
    BrandSerializer,
    ProductVariantSerializer,
    WishListSerializer,
    ProductReviewSerializer,
    ProductRatingSerializer,
)
from product_service.models import Product, Category, Brand, WishList, ProductReview
from product_service.filters import ProductFilter
from haystack.query import SearchQuerySet
import ast
from django.core.cache import cache

"""
10 days is the default timeout for wishlist.
"""
DEFAULT_WISHLIST_REDIS_TIMEOUT = 10 * 60 * 60 * 24


class RoutesAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET` requests providing the list of supported `Product Service` API's.
    """

    queryset = routes

    def get(self, request):
        return Response(self.get_queryset())


class ProductAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET` and `POST` requests related to the `Product` model.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset = Product.objects.select_related("category", "brand").all().order_by("name")
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get(self, request):
        products = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        product_variant_serializer = ProductVariantSerializer(
            data=request.data.get("product_variants"), many=True
        )

        if serializer.is_valid() and product_variant_serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(
            serializer.errors or product_variant_serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductByIdAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET`, `PATCH` and `DELETE` requests related to a `Product` model's instance.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_object(self, id):
        try:
            return Product.objects.get(id=id)
        except Product.DoesNotExist:
            response = {"message": "Unable to find product with id " + str(id)}
            raise NotFound(response)

    def get(self, request, id):
        product = self.get_object(id)
        serializer = self.serializer_class(product, many=False)
        return Response(serializer.data)

    def patch(self, request, id):
        product = self.get_object(id)
        serializer = self.serializer_class(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET` and `POST` requests related to the `Category` model.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.root_nodes()
    filter_backends = [DjangoFilterBackend]

    def get(self, request):
        categories = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryByIdAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET`, `PATCH` and `DELETE` requests related to a `Category` model's instance.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_object(self, id):
        try:
            return Category.objects.get(id=id)
        except Category.DoesNotExist:
            response = {"message": "Unable to find category with id " + str(id)}
            raise NotFound(response)

    def get(self, request, id):
        category = self.get_object(id)
        serializer = self.serializer_class(category, many=False)
        return Response(serializer.data)

    def patch(self, request, id):
        category = self.get_object(id)
        serializer = self.serializer_class(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        category = self.get_object(id)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BrandAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET` and `POST` requests related to the `Brand` model.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

    def get(self, request):
        brands = self.get_queryset()
        serializer = self.serializer_class(brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BrandByIdAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET`, `PATCH` and `DELETE` requests related to a `Brand` model's instance.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BrandSerializer

    def get_object(self, id):
        try:
            return Brand.objects.get(id=id)
        except Brand.DoesNotExist:
            response = {"message": "Unable to find brand with id " + str(id)}
            raise NotFound(response)

    def get(self, request, id):
        brand = self.get_object(id)
        serializer = self.serializer_class(brand, many=False)
        return Response(serializer.data)

    def patch(self, request, id):
        brand = self.get_object(id)
        serializer = self.serializer_class(brand, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        brand = self.get_object(id)
        brand.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategorySearchAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET` requests which queries the `Solr` instance to get the related categories.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q", "")
        search_results = SearchQuerySet().filter(text__contains=query)
        results = []

        for result in search_results:
            """
            e.g., result.id = "product_service.category.1".
            We split the string based on "." and take the integer part as id.
            """
            id = int(result.id.split(".")[2])
            """ e.g., result.text = "['Men']". We convert to Python list and take the first element in it. """
            name = ast.literal_eval(result.text)[0]
            """ e.g., result.slug = "['men']". We convert to Python list and take the first element in it. """
            slug = ast.literal_eval(result.slug)[0]
            results.append({"id": id, "name": name, "slug": slug})

        return Response(results, status=status.HTTP_200_OK)


class WishListAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET` and `POST` requests related to the `Wishlist` model.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer

    def get_object(self):
        return self.request.user

    def get_redis_cache_key(self):
        return "user:{user}:wishlist".format(user=self.get_object())

    def get_queryset(self):
        user = self.get_object()
        return WishList.objects.filter(user=user).order_by("updated_at")

    def get(self, request):
        if not cache.has_key(self.get_redis_cache_key()):
            wishlisted_products = self.get_queryset()
            serializer = self.serializer_class(wishlisted_products, many=True)
            """
            Set the serialized data in redis cache with key format set to user:<user email>:wishlist
            and timeout as 10 days.
            """
            cache.set(self.get_redis_cache_key(), serializer.data, DEFAULT_WISHLIST_REDIS_TIMEOUT)
            return Response(serializer.data)

        """ Return the cached response """
        return Response(cache.get(self.get_redis_cache_key()))

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={"user": self.get_object()})
        if serializer.is_valid():
            serializer.validated_data["user"] = self.get_object()
            serializer.save()

            # Delete the existing cached wishlist in redis
            if cache.has_key(self.get_redis_cache_key()):
                cache.delete(self.get_redis_cache_key())

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishListByIdAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET` and `DELETE` requests related to a `Wishlist` model's instance.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = WishListSerializer

    def get_object(self, id):
        try:
            return WishList.objects.get(id=id)
        except WishList.DoesNotExist:
            response = {"message": "Unable to find wishlist product with id " + str(id)}
            raise NotFound(response)

    def get_redis_cache_key(self):
        return "user:{user}:wishlist".format(user=self.request.user)

    def get(self, request, id):
        wishlisted_product = self.get_object(id)
        serializer = self.serializer_class(wishlisted_product, many=False)
        return Response(serializer.data)

    def delete(self, request, id):
        wishlisted_product = self.get_object(id)
        wishlisted_product.delete()

        # Delete the existing cached wishlist in redis
        if cache.has_key(self.get_redis_cache_key()):
            cache.delete(self.get_redis_cache_key())

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductReviewAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `POST` requests related to the `ProductReview` model.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProductReviewSerializer

    def get_object(self):
        return self.request.user

    def get_queryset(self, **kwargs):
        if not Product.objects.filter(id=kwargs["product_id"]).exists():
            response = {"message": f"Unable to find product with id {kwargs['product_id']}"}
            raise NotFound(response)

        return ProductReview.objects.filter(product=kwargs["product_id"]).order_by("-created_at")

    def get(self, request, **kwargs):
        product_reviews = self.get_queryset(**kwargs)
        serializer = self.serializer_class(product_reviews, many=True)
        return Response(serializer.data)

    def post(self, request, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if not Product.objects.filter(id=kwargs["product_id"]).exists():
            response = {"message": f"Unable to find product with id {kwargs['product_id']}"}
            raise NotFound(response)

        if serializer.is_valid():
            serializer.validated_data["user"] = self.get_object()
            serializer.validated_data["product"] = Product.objects.get(id=kwargs["product_id"])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReviewByIdAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET`, `PATCH` and `DELETE` requests related to the `ProductReview` model.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProductReviewSerializer

    def get_object(self, **kwargs):
        try:
            return ProductReview.objects.get(product=kwargs["product_id"], id=kwargs["id"])
        except ProductReview.DoesNotExist:
            response = {
                "message": f"Unable to find review with id {kwargs['id']} for product {kwargs['product_id']}"
            }
            raise NotFound(response)

    def get(self, request, **kwargs):
        product_review = self.get_object(**kwargs)
        serializer = self.serializer_class(product_review, many=False)
        return Response(serializer.data)

    def patch(self, request, **kwargs):
        product_review = self.get_object(**kwargs)
        serializer = self.serializer_class(product_review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        product_review = self.get_object(**kwargs)
        product_review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductRatingAPIView(generics.GenericAPIView):
    """
    API View for handling HTTP `GET` requests for the product rating metrics.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = ProductRatingSerializer

    def get_object(self, **kwargs):
        try:
            return Product.objects.get(id=kwargs["product_id"])
        except Product.DoesNotExist:
            response = {"message": f"Unable to find product with id {kwargs['product_id']}"}
            raise NotFound(response)

    def get(self, request, **kwargs):
        product = self.get_object(**kwargs)
        serializer = self.serializer_class(product, many=False)
        return Response(serializer.data)
