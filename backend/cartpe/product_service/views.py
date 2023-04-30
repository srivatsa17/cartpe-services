from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from .routes import routes
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer
from .models import Product, Category, Brand
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter

# Create your views here.

class RoutesAPIView(generics.GenericAPIView):
    queryset = routes

    def get(self, request):
        return Response(self.get_queryset())

class ProductAPIView(generics.GenericAPIView):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()
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
        response = { "message" : "Product '" + product.name + "' deleted successfully." }
        return Response(response, status = status.HTTP_204_NO_CONTENT)

class CategoryAPIView(generics.GenericAPIView):

    serializer_class = CategorySerializer
    queryset = Category.objects.root_nodes()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

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
        response = { "message" : "Category '" + category.name + "' deleted successfully." }
        return Response(response, status = status.HTTP_204_NO_CONTENT)
    
class BrandAPIView(generics.GenericAPIView):

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
        response = { "message" : "Brand '" + brand.name + "' deleted successfully." }
        return Response(response, status = status.HTTP_204_NO_CONTENT)