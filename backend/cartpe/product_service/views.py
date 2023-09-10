from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from product_service.routes import routes
from product_service.serializers import ProductSerializer, CategorySerializer, BrandSerializer, ProductImageSerializer
from product_service.models import Product, Category, Brand, Image
from product_service.filters import ProductFilter, CategoryFilter
from haystack.query import SearchQuerySet
import ast

# Create your views here.

class RoutesAPIView(generics.GenericAPIView):
    queryset = routes

    def get(self, request):
        return Response(self.get_queryset())

class ProductAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer
    queryset =  (
                    Product.objects
                    .select_related('category', 'brand')
                    .prefetch_related('attributes__attribute_values', 'product_images')
                    .all()
                    .order_by('name')
                )
    filter_backends = [ DjangoFilterBackend ]
    filterset_class = ProductFilter

    def get(self, request):
        products = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(products, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProductByIdAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_object(self, id):
        try:
            return Product.objects.get(id = id)
        except Product.DoesNotExist:
            response = { "message" : "Unable to find product with id " + str(id) }
            raise NotFound(response)

    def get(self, request, id):
        product = self.get_object(id)
        serializer = self.serializer_class(product, many = False)
        return Response(serializer.data)

    def patch(self, request, id):
        product = self.get_object(id)
        serializer = self.serializer_class(product, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        product = self.get_object(id)
        product.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class CategoryAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.root_nodes()
    filter_backends = [ DjangoFilterBackend ]
    filterset_class = CategoryFilter

    def get(self, request):
        categories = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(categories, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class CategoryByIdAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_object(self, id):
        try:
            return Category.objects.get(id = id)
        except Category.DoesNotExist:
            response = { "message" : "Unable to find category with id " + str(id) }
            raise NotFound(response)

    def get(self, request, id):
        category = self.get_object(id)
        serializer = self.serializer_class(category, many = False)
        return Response(serializer.data)

    def patch(self, request, id):
        category = self.get_object(id)
        serializer = self.serializer_class(category, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        category = self.get_object(id)
        category.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class BrandAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()

    def get(self, request):
        brands = self.get_queryset()
        serializer = self.serializer_class(brands, many = True)
        return Response(serializer.data)

    def post(self, request):
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BrandByIdAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BrandSerializer

    def get_object(self, id):
        try:
            return Brand.objects.get(id = id)
        except Brand.DoesNotExist:
            response = { "message" : "Unable to find brand with id " + str(id) }
            raise NotFound(response)

    def get(self, request, id):
        brand = self.get_object(id)
        serializer = self.serializer_class(brand, many = False)
        return Response(serializer.data)

    def patch(self, request, id):
        brand = self.get_object(id)
        serializer = self.serializer_class(brand, data = request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        brand = self.get_object(id)
        brand.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class ProductImageAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductImageSerializer

    def get_object(self, id):
        try:
            return Product.objects.get(id = id)
        except Product.DoesNotExist:
            response = { "message" : "Unable to find product with id " + str(id) }
            raise NotFound(response)

    def get_queryset(self):
        if not self.request.query_params:
            response = { "message" : "Please make sure query params are sent in the format ?product=<id>." }
            raise ParseError(response)

        productPathParam = self.request.query_params.get('product')

        if not productPathParam.isnumeric():
            response = { "message" : "Please enter a valid integer for product id." }
            raise ParseError(response)

        product = self.get_object(productPathParam)
        images = Image.objects.filter(product = product)
        return images

    def get(self, request):
        images = self.get_queryset()
        serializer = self.serializer_class(images, many = True)
        return Response(serializer.data)

    def post(self, request):
        images = self.get_queryset()
        serializer = self.serializer_class(data = request.data, context = self.request.query_params)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ProductImageByIdAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductImageSerializer

    def get_object(self, id):
        try:
            return Image.objects.get(id = id)
        except Image.DoesNotExist:
            response = { "message" : "Unable to find image with id " + str(id) }
            raise NotFound(response)

    def get(self, request, id):
        image = self.get_object(id)
        serializer = self.serializer_class(image, many = False)
        return Response(serializer.data)

    def patch(self, request, id):
        image = self.get_object(id)
        serializer = self.serializer_class(image, data = request.data, context = { 'imageId':id }, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        image = self.get_object(id)
        image.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)

class CategorySearchAPIView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('q', '')
        search_results = SearchQuerySet().filter(text__contains = query)
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
            results.append(
                {
                    "id": id,
                    "name" : name,
                    "slug": slug
                }
            )

        return Response(results, status = status.HTTP_200_OK)