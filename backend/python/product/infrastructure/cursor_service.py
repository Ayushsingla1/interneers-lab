from base64 import b64decode, urlsafe_b64encode
from datetime import datetime
import json
from product.domain.custom_exceptions import InvalidCursorError
from product.application.ports.outgoing.cursor_ports import (
    CursorPaginationPorts,
    DecodedCursor,
)


class CursorPagination(CursorPaginationPorts):

    def __init__(self):
        self.required_keys = ["id", "created_at"]

    def encode(self, id: str, created_at: datetime) -> str:
        try:
            json_details = json.dumps({"id": id, "created_at": created_at.isoformat()})

            next_cursor = urlsafe_b64encode(json_details.encode("utf-8")).decode(
                "utf-8"
            )
            return next_cursor
        except Exception as e:
            raise InvalidCursorError("Token sent is invalid")

    def decode(self, cursor: str) -> DecodedCursor:
        try:
            details = json.loads(b64decode(cursor).decode("utf-8"))

            if all(key in details for key in self.required_keys):
                id = details["id"]
                created_at = datetime.fromisoformat(details["created_at"])
                return DecodedCursor(id=id, created_at=created_at)
            else:
                raise InvalidCursorError("Token sent is invalid")
        except Exception:
            raise InvalidCursorError(f"Token sent is invalid")
