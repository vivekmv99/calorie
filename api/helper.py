
import jwt

def token_decode(request):
    token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
    decoded = jwt.decode(token, options={"verify_signature": False})
    return decoded