from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from product_service.models import Image, Product

class ProductModelTest(TestCase):
    def setUp(self) -> None:
        self.product = Product.objects.create(name="Canon 80 D", description="good product", price=50000, stock_count=10)
        self.sampleImage = "https://cartpe.s3.ap-south-1.amazonaws.com/Products/Canon+80D/canon_80D_image_1.webp"
        self.imageInstance = Image.objects.create(image=self.sampleImage, is_featured=True, product=self.product)

    def test_str_is_equal_to_title(self) -> None:
        imageObj = Image.objects.get(id = self.imageInstance.id)
        expectedResponse = imageObj.image
        receivedResponse = str(imageObj)

        self.assertEqual(receivedResponse, expectedResponse)