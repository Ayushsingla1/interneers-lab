from product.domain.custom_exceptions import InvalidIdError
from bson import ObjectId as BsonObjectID
from mongoengine.fields import ObjectId


def _validate_object_id(value: str, label: str = "Id"):

    if not value or not isinstance(value, str):
        raise InvalidIdError(f"{label} must be a non-empty string")
    if not BsonObjectID.is_valid(value):
        raise InvalidIdError(f"{label} '{value}' is not a valid ObjectId")

    return ObjectId(value)
