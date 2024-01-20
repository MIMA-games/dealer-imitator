import secrets
import datetime
import calendar

from typing import Type
from bson import ObjectId


def singleton(class_):
    """
    singleton decorator for preventing developers
    creating more than one instance of the class.
    """
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


def generate_api_key(length: int = 80) -> str:
    return secrets.token_urlsafe(length)


def get_timestamp(plus_seconds: int = 0):
    return calendar.timegm(datetime.datetime.utcnow().utctimetuple()) + plus_seconds


def mongo_converter(model_cls: Type):
    def wrapper(func):
        async def wrapped_func(*args, **kwargs):
            try:
                data = kwargs.get("data") or args[1]
            except IndexError:
                data = None
            if data and isinstance(data, dict) and "id" in data:
                data["_id"] = ObjectId(data.pop("id"))

            result = await func(*args, **kwargs)

            if isinstance(result, list):
                final_list = []
                for document in result:
                    document["id"] = str(document.pop("_id"))
                    final_list.append(model_cls(**document))
                return final_list
            elif isinstance(result, dict) and "_id" in result:
                result["id"] = str(result.pop("_id"))
            return model_cls(**result) if result else None

        return wrapped_func

    return wrapper
