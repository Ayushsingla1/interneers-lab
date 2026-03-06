import unittest
from unittest import TestCase
from unittest.mock import MagicMock

from .product_service import ProductServices


def make_products(id="123", name="speaker", description="something cool"):
    mock = MagicMock()
    mock.id = id
    mock.name = f"speaker{id}"
    mock.description = description

    return mock


class TestProductService(TestCase):
    def setUp(self) -> None:
        self.mock_repo = MagicMock()
        self.service = ProductServices(repository=self.mock_repo)

    def test_get_all_success(self):

        products = [make_products(str(i)) for i in range(0, 3)]
        self.mock_repo.get_all.return_value = products

        result = self.service.get_all(page=2, limit=10)

        self.assertEqual(result, products)
        self.mock_repo.get_all.assert_called_once_with(start=10, end=20)

    def test_get_by_id_success(self):

        products = make_products(id="1")
        self.mock_repo.get_by_id.return_value = products

        result = self.service.get_by_id(id="1")

        self.assertEqual(result, products)
        self.mock_repo.get_by_id.assert_called_once_with("1")

    def test_add_success(self):

        product = make_products("1")
        kwargs = {"name": "speaker", "description": "something cool"}
        self.mock_repo.add.return_value = product

        result = self.service.add(**kwargs)

        self.assertEqual(result, product)
        self.mock_repo.add.assert_called_once_with(**kwargs)

    def test_delete_success(self):

        # self.mock_repo.delete
        self.service.delete("1")

        self.mock_repo.delete.assert_called_once_with("1")

    def test_update_success(self):

        kwargs = {"name": "speaker", "description": "something cool"}

        self.service.update("1", **kwargs)

        called_kwargs = {"set__name": "speaker", "set__description": "something cool"}
        self.mock_repo.update.assert_called_once_with("1", **called_kwargs)


if __name__ == "__main__":
    unittest.main()
