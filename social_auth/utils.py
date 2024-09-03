import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

def Firebase_validation(id_token):
   """
   This function receives id token sent by Firebase and
   validate the id token then check if the user exist on
   Firebase or not if exist it returns True else False
   """


   decoded_token = auth.verify_id_token(id_token)
   uid = decoded_token['uid']
   provider = decoded_token['firebase']['sign_in_provider']
   image = None
   name = None
   if "name" in decoded_token:
      name = decoded_token['name']
   if "picture" in decoded_token:
        image = decoded_token['picture']
   try:
        user = auth.get_user(uid)
        email = user.email
        if user:
            return {
                "status": True,
                "uid": uid,
                "email": email,
                "name": name,
                "provider": provider,
                "image": image
            }
        else:
            return False
   except Exception:
        print("user not exist")
