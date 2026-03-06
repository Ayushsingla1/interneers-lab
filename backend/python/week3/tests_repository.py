import unittest
from unittest import TestCase
from unittest.mock import MagicMock, patch

from mongoengine import DoesNotExist

from .product_repository import (
    ProductNotFoundError,
    ProductRepository,
    ProductRepositoryError,
)


# Create your tests here.
#
def make_products(id="123", name="speaker", description="something cool"):
    mock = MagicMock()
    mock.id = id
    mock.name = f"speaker{id}"
    mock.description = description

    return mock


class TestProductRepository(TestCase):
    def setUp(self) -> None:
        self.repo = ProductRepository()
        self.kwargs = {"name": "speaker1", "description": "something cool"}
        self.uid = "1"

    # def tearDown(self) -> None:
    #     return super().tearDown()

    @patch("week3.product_repository.Product")
    def test_get_all(self, mock_get):
        products = [make_products(id=str(i)) for i in range(0, 3)]
        mock_get.objects.__getitem__.return_value = products

        result = self.repo.get_all(start=0, end=3)

        self.assertEqual(result, products)

    @patch("week3.product_repository.Product")
    def test_get_all_raise_repository_error(self, mock_get):
        mock_get.objects.__getitem__.side_effect = Exception("db down")

        with self.assertRaises(ProductRepositoryError) as context:
            self.repo.get_all(start=0, end=3)

        self.assertTrue("Unable to fetch Products." in str(context.exception))

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_get_by_id_success(self, mock_get, mock_object_id):
        product = make_products(self.uid)
        mock_get.objects.get.return_value = product
        mock_object_id.return_value = self.uid

        result = self.repo.get_by_id(id=self.uid)

        self.assertEqual(result, product)
        mock_get.objects.get.assert_called_once_with(id=self.uid)

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_get_by_id_raise_product_not_found(self, mock_get, mock_object_id):
        mock_get.objects.get.side_effect = DoesNotExist("not found")

        with self.assertRaises(ProductNotFoundError) as context:
            self.repo.get_by_id(self.uid)

        self.assertTrue("No product with matching Id" in str(context.exception))

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_get_by_id_raise_product_repository_error(self, mock_get, mock_object_id):
        mock_get.objects.get.side_effect = Exception("not found")

        with self.assertRaises(ProductRepositoryError) as context:
            self.repo.get_by_id(self.uid)

        self.assertTrue("Unable to fetch Product" in str(context.exception))

    @patch("week3.product_repository.Product")
    def test_add_success(self, mock_get):
        product = make_products(self.uid)
        mock_get.return_value = product

        result = self.repo.add(**self.kwargs)

        self.assertEqual(result, product)
        mock_get.assert_called_once_with(**self.kwargs)
        product.save.assert_called_once()

    @patch("week3.product_repository.Product")
    def test_add_raise_product_repository_error(self, mock_get):

        product = make_products(self.uid)
        mock_get.return_value = product

        product.save.side_effect = Exception("db down")

        with self.assertRaises(ProductRepositoryError) as context:
            self.repo.add(**self.kwargs)

        self.assertTrue("Unable to save product" in str(context.exception))

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_delete_success(self, mock_get, mock_object_id):
        mock_object_id.return_value = self.uid
        mock_get.objects.return_value.delete.return_value = 1

        self.repo.delete(id=self.uid)

        mock_object_id.assert_called_once_with(self.uid)
        mock_get.objects.return_value.delete.assert_called_once_with()

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_delete_raises_product_not_found_error(self, mock_get, mock_object_id):

        mock_object_id.return_value = self.uid
        mock_get.objects.return_value.delete.return_value = 0

        with self.assertRaises(ProductNotFoundError):
            self.repo.delete(id=self.uid)

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_delete_raises_product_repository_error(self, mock_get, mock_object_id):
        mock_object_id.return_value = self.uid
        mock_get.objects.return_value.delete.side_effect = Exception("db down")

        with self.assertRaises(ProductRepositoryError):
            self.repo.delete(id=self.uid)

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_update_success(self, mock_get, mock_object_id):
        mock_object_id.return_value = self.uid
        mock_get.objects.return_value.update_one.return_value = 1

        self.repo.update(id=self.uid, **self.kwargs)
        mock_object_id.assert_called_once_with(self.uid)
        mock_get.objects.return_value.update_one.assert_called_once_with(**self.kwargs)

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_update_raises_product_not_found_error(self, mock_get, mock_object_id):
        mock_object_id.return_value = self.uid
        mock_get.objects.return_value.update_one.return_value = 0

        with self.assertRaises(ProductNotFoundError):
            self.repo.update(id=self.uid, **self.kwargs)

    @patch("week3.product_repository.ObjectId")
    @patch("week3.product_repository.Product")
    def test_update_raises_product_repository_error(self, mock_get, mock_object_id):
        mock_object_id.return_value = self.uid
        mock_get.objects.return_value.update_one.side_effect = Exception("db down")

        with self.assertRaises(ProductRepositoryError):
            self.repo.update(id=self.uid, **self.kwargs)


if __name__ == "__main__":
    unittest.main()
