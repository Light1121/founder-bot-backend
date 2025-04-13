import datetime
import json
from uuid import UUID


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        elif isinstance(obj, UUID):
            return str(obj)
        else:
            return super().default(obj)