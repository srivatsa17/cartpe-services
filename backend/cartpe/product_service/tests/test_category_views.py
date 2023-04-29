from django.test import Client
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import json
from ..models import Category
from ..serializers import CategorySerializer

# Create your tests here.

# Initialize the APIClient app
client = Client()

class GetAllCategoriesTest(APITestCase):
    """ Test module for GET all categories API """

    def setUp(self) -> None:
        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)
        self.topwear = Category.objects.create(name = "Topwear", description = "Topwear for men", parent = self.men)

    def test_get_all_categories(self) -> None:
        response = client.get(reverse('categories'))
        categories = Category.objects.root_nodes()
        serializer = CategorySerializer(categories, many = True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class GetCategoryByIdTest(APITestCase):
    """ Test module for GET category by id API """

    def setUp(self) -> None:
        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)
        self.topwear = Category.objects.create(name = "Topwear", description = "Topwear for men", parent = self.men)

    def test_get_category_by_id_with_valid_id(self) -> None:
        response = client.get(reverse('category_by_id', kwargs = { 'id' : self.men.id }))
        category = Category.objects.get(id = self.men.pk)
        serializer = CategorySerializer(category, many = False)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_by_id_with_non_existing_id(self) -> None:
        response = client.get(reverse('category_by_id', kwargs = { 'id' : 30 }))

        self.assertEqual(response.data['message'], "Unable to find category with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class PostCategoryTest(APITestCase):
    """ Test module for Post a category API """

    def setUp(self) -> None:
        self.validData = { "name":"Men", "description":"Clothing for men", "parent":None }
        self.subcategory = { "name":"Topwear", "description":"Topwear for men", "parent":"Men"}
        self.dataWithNoNameField = { "description":"Clothing for men", "parent" : None }
        self.dataWithNoDescriptionField = { "name":"Men", "parent" : None }
        self.dataWithNoParentField = { "name":"Men", "description":"Clothing" }
        self.dataWithExistingNameAndParent = self.validData

    def test_post_category_with_valid_data(self) -> None:
        response = client.post(reverse('categories'), data = json.dumps(self.validData), content_type = 'application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_category_with_subcategory(self) -> None:
        client.post(reverse('categories'), data = json.dumps(self.validData), content_type = 'application/json')
        response = client.post(reverse('categories'), data = json.dumps(self.subcategory), content_type = 'application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_category_with_missing_name(self) -> None:
        response = client.post(reverse('categories'), data = json.dumps(self.dataWithNoNameField), content_type = 'application/json')

        self.assertEqual(response.data['name'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_category_with_missing_description(self) -> None:
        response = client.post(reverse('categories'), data = json.dumps(self.dataWithNoDescriptionField), content_type = 'application/json')

        self.assertEqual(response.data['description'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_category_with_missing_parent(self) -> None:
        response = client.post(reverse('categories'), data = json.dumps(self.dataWithNoParentField), content_type = 'application/json')

        self.assertEqual(response.data['parent'][0], "This field is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_category_with_nonexisting_parent(self) -> None:
        response = client.post(reverse('categories'), data = json.dumps(self.subcategory), content_type = 'application/json')

        self.assertEqual(response.data['parent'][0], "Object with name=Men does not exist.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_category_with_same_name_and_parent_combination(self) -> None:
        client.post(reverse('categories'), data = json.dumps(self.validData), content_type = 'application/json')
        response = client.post(reverse('categories'), data = json.dumps(self.dataWithExistingNameAndParent), content_type = 'application/json')

        self.assertEqual(response.data['message'][0], "The fields name, parent must make a unique set.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class UpdateCategoryByIdTest(APITestCase):
    """ Test module for Update a category API """

    def setUp(self) -> None:
        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)
        self.women = Category.objects.create(name = "Women", description = "Clothing for women", parent = None)
        self.topwear = Category.objects.create(name = "Topwear", description = "Topwear for men", parent = self.men)
        self.footwear = Category.objects.create(name = "Footwear", description = "Footwear for men", parent = self.men)
        self.updateId = { "id" : 20 }
        self.updateName = { "name" : "abc" }
        self.updateDescription = { "description" : "good one" }
        self.updateSlug = { "slug" : "abcd" }
        self.updateParent = { "parent" : "Clothes" }
        self.updateChild = { "parent" : "Women" }
        self.invalidName = { "name" : "" }
        self.existingNameAndParent = { "name" : "Footwear", "parent" : "Men" }
        self.existingNameAndParentEqualToNone = { "name" : "men", "parent" : None }

    def test_update_category_id(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id' : self.men.id}), data = json.dumps(self.updateId), content_type = 'application/json')

        self.assertEqual(response.data['id'], self.men.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_name(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id' : self.men.id}), data = json.dumps(self.updateName), content_type = 'application/json')

        self.assertEqual(response.data['name'], "abc")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_description(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id' : self.men.id}), data = json.dumps(self.updateDescription), content_type = 'application/json')

        self.assertEqual(response.data['description'], self.updateDescription['description'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_slug(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id' : self.men.id}), data = json.dumps(self.updateSlug), content_type = 'application/json')

        self.assertEqual(response.data['slug'], self.men.slug)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_category_parent(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id' : self.men.id}), data = json.dumps(self.updateParent), content_type = 'application/json')

        self.assertEqual(response.data['parent'][0], "Object with name=Clothes does not exist.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category_child(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id' : self.topwear.id}), data = json.dumps(self.updateChild), content_type = 'application/json')

        self.assertEqual(response.data['parent'], "Women")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_name_with_empty_input(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id': self.men.id}), data = json.dumps(self.invalidName), content_type = 'application/json')

        self.assertEqual(response.data['name'][0], "This field may not be blank.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category_with_nonexisting_id(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs = {'id': 30}), data = json.dumps(self.invalidName), content_type = 'application/json')

        self.assertEqual(response.data['message'], "Unable to find category with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_category_with_existing_name_and_parent(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id': self.topwear.id}), data = json.dumps(self.existingNameAndParent), content_type = 'application/json')
    
        self.assertEqual(response.data['message'][0], "The fields name, parent must make a unique set.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_category_with_same_name_and_parent_equal_to_null(self) -> None:
        response = client.patch(reverse('category_by_id', kwargs={'id': self.men.id}), data = json.dumps(self.existingNameAndParentEqualToNone), content_type = 'application/json')

        self.assertEqual(response.data['message'][0], "The fields name, parent must make a unique set.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteCategoryByIdTest(APITestCase):
    """ Test module for Delete a category API """

    def setUp(self) -> None:
        self.men = Category.objects.create(name = "Men", description = "Clothing", parent = None)

    def test_delete_with_existing_id(self) -> None:
        response = client.delete(reverse('category_by_id', kwargs={'id': self.men.id}))

        self.assertEqual(response.data['message'], "Category 'Men' deleted successfully.")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_with_nonexisting_id(self) -> None:
        response = client.delete(reverse('product_by_id', kwargs={'id': 30}))

        self.assertEqual(response.data['message'], "Unable to find product with id 30")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)