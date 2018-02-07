import uuid


def get_request_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    return ip if ip else "127.0.0.1"


def generate_32_uuid():
    session_key = uuid.uuid1()
    return str(session_key).replace("-", "")