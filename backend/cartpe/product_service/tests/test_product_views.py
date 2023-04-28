from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json, decimal
from ..models import Product, Category
from ..serializers import ProductSerializer

# Create your tests here.

# Initialize the APIClient app
client = Client()

class GetAllProductsTest(APITestCase):
    """ Test module for GET all products API """

    def setUp(self) -> None:
        Product.objects.create(name = "iphone 13", description = "ok product", brand = "apple", price = 70000, stock_count = 1)
        Product.objects.create(name = "pixel 7", description = "good product", brand = "google", price = 50000, stock_count = 10)

    def test_get_all_products(self) -> None:
        response = client.get(reverse('products'))
        products = Product.objects.all()
        serializer = ProductSerializer(products, many = True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetProductByIdTest(APITestCase):
    """ Test module for GET product by id API """

    def setUp(self) -> None:
        self.iphone = Product.objects.create(name = "iphone 13", description = "ok product", brand = "apple", price = 70000, stock_count = 1)
        self.pixel = Product.objects.create(name = "pixel 7", description = "good product", brand = "google", price = 50000, stock_count = 10)

    def test_get_product_by_id_with_valid_id(self) -> None:
        response = client.get(reverse('product_by_id', kwargs = { 'id' : self.pixel.id }))
        product = Product.objects.get(id = self.pixel.pk)
        serializer = ProductSerializer(product, many = False)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_product_by_id_with_non_existing_id(self) -> None:
        response = client.get(reverse('product_by_id', kwargs = { 'id' : 30 }))

        self.assertEqual(response.data['message'], "Unable to find product with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PostProductTest(APITestCase):
    """ Test module for Post a product API """

    def setUp(self) -> None:
        self.category = Category.objects.create(name = "Electronics")
        self.validData = { "name":"DSLR", "description":"Amazing", "brand":"Cannon", "category":"Electronics", "price":929.99, "stock_count":5, "discount":0 }
        self.dataWithNoNameField = { "description":"Amazing", "brand":"Cannon", "category":"Electronics", "price":929.99, "stock_count":5, "discount":0 }
        self.dataWithNoDescriptionField = { "name":"DSLR", "brand":"Cannon", "category":"Electronics", "price":929.99, "stock_count":5, "discount":0 }
        self.dataWithNoPriceField = { "name":"DSLR", "description":"Amazing", "brand":"Cannon", "category":"Electronics", "stock_count":5, "discount":0 }
        self.dataWithNoBrandField = { "name":"DSLR", "description":"Amazing", "category":"Electronics", "price":929.99, "stock_count":5, "discount":0 }
        self.dataWithNoStockCountField = { "name":"DSLR", "description":"Amazing", "brand":"Cannon", "category":"Electronics", "price":929.99, "discount":0 }
        self.dataWithNoDiscountField = { "name":"DSLR", "description":"Amazing", "brand":"Cannon", "category":"Electronics", "price":929.99, "stock_count":5 }
        self.dataWithNoCategoryField = { "name":"DSLR", "description":"Amazing", "brand":"Cannon", "price":929.99, "stock_count":5, "discount":0 }
        self.dataWithExistingName = self.validData

    def test_post_product_with_valid_data(self) -> None:
        response = client.post(reverse('products'), data = json.dumps(self.validData), content_type = 'application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_product_with_missing_name(self) -> None:
        response = client.post(reverse('products'), data = json.dumps(self.dataWithNoNameField), content_type = 'application/json')

        self.assertEqual(response.data['name'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_product_with_missing_description(self) -> None:
        response = client.post(reverse('products'), data = json.dumps(self.dataWithNoDescriptionField), content_type = 'application/json')

        self.assertEqual(response.data['description'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_product_with_missing_price(self) -> None:
        response = client.post(reverse('products'), data = json.dumps(self.dataWithNoPriceField), content_type = 'application/json')

        self.assertEqual(response.data['price'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_product_with_missing_brand(self) -> None:
        response = client.post(reverse('products'), data = json.dumps(self.dataWithNoBrandField), content_type = 'application/json')

        self.assertEqual(response.data['brand'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_product_with_missing_stock_count(self) -> None:
        response = client.post(reverse('products'), data = json.dumps(self.dataWithNoStockCountField), content_type = 'application/json')

        self.assertEqual(response.data['stock_count'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_product_with_missing_discount(self) -> None:
        response = client.post(reverse('products'), data = json.dumps(self.dataWithNoDiscountField), content_type = 'application/json')

        self.assertEqual(response.data['discount'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_product_with_missing_category(self) -> None:
        response = client.post(reverse('products'), data = json.dumps(self.dataWithNoCategoryField), content_type = 'application/json')

        self.assertEqual(response.data['category'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_product_with_same_name(self) -> None:
        client.post(reverse('products'), data = json.dumps(self.validData), content_type = 'application/json')
        response = client.post(reverse('products'), data = json.dumps(self.dataWithExistingName), content_type = 'application/json')

        self.assertEqual(response.data['message'][0], "Product 'DSLR' already exists and cannot be created or updated again.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateProductByIdTest(APITestCase):
    """ Test module for Update a product API """

    def setUp(self) -> None:
        self.category = Category.objects.create(name = "Electronics")
        self.pixel = Product.objects.create(name="pixel 7", description="good product", brand="google" , price=50000, stock_count=10, discount=0)
        self.updateId = { "id" : 20 }
        self.updateName = { "name" : "abc" }
        self.updateSku = { "sku" : "a42c3fa7-a0be-45a9-ae06-61835f2cf64e" }
        self.updateDescription = { "description" : "good phone" }
        self.updateSlug = { "slug" : "abcd" }
        self.updatePrice = { "price" : 70000.90 }
        self.updateBrand = { "brand" : "apple"}
        self.updateStockCount = { "stock_count" : 15}
        self.updateDiscount = { "discount" : 10}
        self.updateCategory = { "category" : "Phone"}
        self.invalidName = { "name" : "" }
        self.existingData = { "name" : "pixel 7"}

    def test_update_product_id(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateId), content_type = 'application/json')

        self.assertEqual(response.data['id'], self.pixel.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_name(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateName), content_type = 'application/json')

        self.assertEqual(response.data['name'], "abc")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_sku(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateSku), content_type = 'application/json')

        self.assertEqual(response.data['sku'], str(self.pixel.sku))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_description(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateDescription), content_type = 'application/json')

        self.assertEqual(response.data['description'], self.updateDescription['description'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_slug(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateSlug), content_type = 'application/json')

        self.assertEqual(response.data['slug'], self.pixel.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_price(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updatePrice), content_type = 'application/json')

        self.assertEqual(response.data['price'], decimal.Decimal('70000.90'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_brand(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateBrand), content_type = 'application/json')

        self.assertEqual(response.data['brand'], "apple")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_stock_count(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateStockCount), content_type = 'application/json')

        self.assertEqual(response.data['stock_count'], 15)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_discount(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateDiscount), content_type = 'application/json')

        self.assertEqual(response.data['discount'], 10)
        self.assertEqual(response.data['discounted_price'], decimal.Decimal('5000'))
        self.assertEqual(response.data['selling_price'], 45000)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_category(self) -> None:
        self.category = Category.objects.create(name = "Phone")
        response = client.patch(reverse('product_by_id', kwargs={'id' : self.pixel.id}), data = json.dumps(self.updateCategory), content_type = 'application/json')

        self.assertEqual(str(response.data['category']), "Phone")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_product_name_with_empty_input(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id': self.pixel.id}), data = json.dumps(self.invalidName), content_type = 'application/json')

        self.assertEqual(response.data['name'][0], "This field may not be blank.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_with_nonexisting_id(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs = {'id': 30}), data = json.dumps(self.invalidName), content_type = 'application/json')

        self.assertEqual(response.data['message'], "Unable to find product with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_with_same_name(self) -> None:
        response = client.patch(reverse('product_by_id', kwargs={'id': self.pixel.id}), data = json.dumps(self.existingData), content_type = 'application/json')

        self.assertEqual(response.data['message'][0], "Product 'pixel 7' already exists and cannot be created or updated again.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteProductByIdTest(APITestCase):
    """ Test module for Delete a product API """

    def setUp(self) -> None:
        self.pixel = Product.objects.create(name = "pixel 7", description = "good product", brand = "google", price = 50000, stock_count = 10)

    def test_delete_with_existing_id(self) -> None:
        response = client.delete(reverse('product_by_id', kwargs={'id': self.pixel.id}))

        self.assertEqual(response.data['message'], "Product 'pixel 7' deleted successfully.")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_with_nonexisting_id(self) -> None:
        response = client.delete(reverse('product_by_id', kwargs={'id': 30}))

        self.assertEqual(response.data['message'], "Unable to find product with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)