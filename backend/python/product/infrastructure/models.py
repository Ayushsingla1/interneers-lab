from datetime import UTC, datetime
from typing import ClassVar

from mongoengine import NULLIFY, DecimalField, Document, IntField, QuerySet, StringField
from mongoengine.fields import DateTimeField, ReferenceField


class CategoryDoument(Document):
    title = StringField(max_length=100)
    description = StringField(max_length=255)


class ProductDocument(Document):
    objects: ClassVar[QuerySet]

    name = StringField(max_length=100)
    description = StringField()
    category = ReferenceField(CategoryDoument, reverse_delete_rule=NULLIFY)
    price = DecimalField(precision=2, min_value=0)
    quantity = IntField(min_value=0)
    brand = StringField(unique_with="name")
    created_at = DateTimeField(default=datetime.now(tz=UTC))
    updated_at = DateTimeField(default=datetime.now(tz=UTC))

    meta = {
        "indexes": [
            "brand",
            "name",
            "category",
        ],
    }
