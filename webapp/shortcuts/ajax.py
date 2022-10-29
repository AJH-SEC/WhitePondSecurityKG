
import json
from django.http import HttpResponse


def ajax_success(data=None, **kwargs):
    if data is None:
        data = kwargs
    return_json = json.dumps({"data": data, "success": True})
    response = HttpResponse(return_json, content_type="application/json")
    response['Cache-Control'] = 'no-cache'
    return response


def ajax_error(error_message, data=None, **kwargs):
    if data is None:
        data = kwargs or None
    if data:
        return_json = json.dumps({
            "data": data,
            "success": False,
            "error_message": error_message,
        })
    else:
        return_json = json.dumps({
            "success": False,
            "error_message": error_message,
        })
    response = HttpResponse(return_json, content_type="application/json")
    response['Cache-Control'] = 'no-cache'
    return response
