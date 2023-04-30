from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json
from ..models import Brand
from ..serializers import BrandSerializer

# Create your tests here.

# Initialize the APIClient app
client = Client()

class GetAllBrandsTest(APITestCase):
    """ Test module for GET all brands API """

    def setUp(self) -> None:
        Brand.objects.create(name = "Apple", description = "ok brand")
        Brand.objects.create(name = "Google", description = "good brand")

    def test_get_all_brands(self) -> None:
        response = client.get(reverse('brands'))
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many = True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetBrandByIdTest(APITestCase):
    """ Test module for GET brand by id API """

    def setUp(self) -> None:
        self.apple = Brand.objects.create(name = "apple", description = "ok brand")
        self.google = Brand.objects.create(name = "google", description = "good brand")

    def test_get_brand_by_id_with_valid_id(self) -> None:
        response = client.get(reverse('brand_by_id', kwargs = { 'id' : self.google.id }))
        brand = Brand.objects.get(id = self.google.pk)
        serializer = BrandSerializer(brand, many = False)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_brand_by_id_with_non_existing_id(self) -> None:
        response = client.get(reverse('brand_by_id', kwargs = { 'id' : 30 }))

        self.assertEqual(response.data['message'], "Unable to find brand with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PostBrandTest(APITestCase):
    """ Test module for Post a brand API """

    def setUp(self) -> None:
        self.validData = { "name":"Google", "description":"Amazing" }
        self.dataWithNoNameField = { "description":"Amazing" }
        self.dataWithNoDescriptionField = { "name":"Google" }
        self.dataWithExistingName = self.validData

    def test_post_brand_with_valid_data(self) -> None:
        response = client.post(reverse('brands'), data = json.dumps(self.validData), content_type = 'application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_brand_with_missing_name(self) -> None:
        response = client.post(reverse('brands'), data = json.dumps(self.dataWithNoNameField), content_type = 'application/json')

        self.assertEqual(response.data['name'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_brand_with_missing_description(self) -> None:
        response = client.post(reverse('brands'), data = json.dumps(self.dataWithNoDescriptionField), content_type = 'application/json')

        self.assertEqual(response.data['description'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_brand_with_same_name(self) -> None:
        client.post(reverse('brands'), data = json.dumps(self.validData), content_type = 'application/json')
        response = client.post(reverse('brands'), data = json.dumps(self.dataWithExistingName), content_type = 'application/json')

        self.assertEqual(response.data['message'][0], "Brand 'Google' already exists and cannot be created or updated again.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateBrandByIdTest(APITestCase):
    """ Test module for Update a brand API """

    def setUp(self) -> None:
        self.google = Brand.objects.create(name="Google", description="good brand")
        self.updateId = { "id" : 20 }
        self.updateName = { "name" : "abc" }
        self.updateDescription = { "description" : "amazing brand" }
        self.updateSlug = { "slug" : "abcd" }
        self.invalidName = { "name" : "" }
        self.existingData = { "name" : "Google"}

    def test_update_brand_id(self) -> None:
        response = client.patch(reverse('brand_by_id', kwargs={'id' : self.google.id}), data = json.dumps(self.updateId), content_type = 'application/json')

        self.assertEqual(response.data['id'], self.google.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_brand_name(self) -> None:
        response = client.patch(reverse('brand_by_id', kwargs={'id' : self.google.id}), data = json.dumps(self.updateName), content_type = 'application/json')

        self.assertEqual(response.data['name'], "abc")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_brand_description(self) -> None:
        response = client.patch(reverse('brand_by_id', kwargs={'id' : self.google.id}), data = json.dumps(self.updateDescription), content_type = 'application/json')

        self.assertEqual(response.data['description'], self.updateDescription['description'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_brand_slug(self) -> None:
        response = client.patch(reverse('brand_by_id', kwargs={'id' : self.google.id}), data = json.dumps(self.updateSlug), content_type = 'application/json')

        self.assertEqual(response.data['slug'], self.google.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_brand_name_with_empty_input(self) -> None:
        response = client.patch(reverse('brand_by_id', kwargs={'id': self.google.id}), data = json.dumps(self.invalidName), content_type = 'application/json')

        self.assertEqual(response.data['name'][0], "This field may not be blank.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_brand_with_nonexisting_id(self) -> None:
        response = client.patch(reverse('brand_by_id', kwargs = {'id': 30}), data = json.dumps(self.invalidName), content_type = 'application/json')

        self.assertEqual(response.data['message'], "Unable to find brand with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_brand_with_same_name(self) -> None:
        response = client.patch(reverse('brand_by_id', kwargs={'id': self.google.id}), data = json.dumps(self.existingData), content_type = 'application/json')

        self.assertEqual(response.data['message'][0], "Brand 'Google' already exists and cannot be created or updated again.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteBrandByIdTest(APITestCase):
    """ Test module for Delete a brand API """

    def setUp(self) -> None:
        self.google = Brand.objects.create(name = "google", description = "good brand")

    def test_delete_with_existing_id(self) -> None:
        response = client.delete(reverse('brand_by_id', kwargs={'id': self.google.id}))

        self.assertEqual(response.data['message'], "Brand 'google' deleted successfully.")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_with_nonexisting_id(self) -> None:
        response = client.delete(reverse('brand_by_id', kwargs={'id': 30}))

        self.assertEqual(response.data['message'], "Unable to find brand with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)