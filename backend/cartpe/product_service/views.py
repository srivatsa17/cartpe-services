from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from .routes import routes
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category

# Create your views here.

class RoutesAPIView(generics.GenericAPIView):
    def get(self, request):
        return Response(routes)

class ProductAPIView(generics.GenericAPIView):

    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
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

    def get(self, request):
        categories = Category.objects.all()
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