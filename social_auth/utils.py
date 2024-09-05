import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from accountapp.models import CustomUser


def generate_username(name):
    base_username = "".join(name.split()).lower()
    username = base_username
    while CustomUser.objects.filter(username=username).exists():
        username = f"{base_username}{random.randint(0, 1000)}"
    return username


def validate_firebase_token(id_token):
    """
    Valide le token Firebase et retourne les informations de l'utilisateur si valide.
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token.get('uid')
        provider = decoded_token.get('firebase', {}).get('sign_in_provider')
        email = decoded_token.get('email')
        name = decoded_token.get('name', '')
        picture = decoded_token.get('picture', '')
        
        if uid and email:
            return {
                "status": True,
                "uid": uid,
                "email": email,
                "name": name,
                "provider": provider,
                "image": picture
            }
        return False
    except Exception as e:
        print(f"Firebase validation error: {e}")
        return False
