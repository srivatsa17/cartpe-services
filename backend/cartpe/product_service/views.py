from rest_framework.response import Response
from rest_framework import generics
from .routes import routes
from .Products.serializers import ProductSerializer
from .models import Product

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
        serializer.is_valid(raise_exception = True)
        serializer.save()

        return Response(serializer.data)