from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from product_service.models import Image, Product

class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(name="pixel 7", description="good product", price=50000, stock_count=10)
        self.sampleImage = SimpleUploadedFile("test_image.jpg", b"binary data for image", content_type="image/jpeg")
        self.imageInstance = Image.objects.create(image=self.sampleImage, is_featured=True, product=self.product)

    def test_str_is_equal_to_title(self) -> None:
        imageObj = Image.objects.get(id = self.imageInstance.id)
        expectedResponse = imageObj.image.url
        receivedResponse = str(imageObj)

        self.assertEqual(receivedResponse, expectedResponse)

    def tearDown(self) -> None:
        self.sampleImage.close()
        self.imageInstance.image.delete()