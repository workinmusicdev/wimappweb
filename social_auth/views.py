from django.shortcuts import render
from requests import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from accountapp.models import CustomUser
from social_auth.serializers import GoogleSocialAuthSerializer, FacebookSocialAuthSerializer, SocialSerializerGoogle
from social_auth.utils import Firebase_validation


# Create your views here.

class SocialSignupAPIView(GenericAPIView):
   """
   api for creating user from social logins
   """
   serializer_class = SocialSerializerGoogle

   def post(self, request):
       # auth_header = request.META.get('HTTP_AUTHORIZATION')

       # if auth_header:
       # "ya29.a0AcM612wi-4bfC1SkC1H8QBn6PkqL1ZvNEtRy_s3c7hio14iZU-xoXqSQ2mWZQWCEGjX9AcO5TcjCoTGIe9FwIFqeZ6_FijOgR7XOdMLbDFmntfod64Rc41gE89alnvNi6qag_2QrKuc_rvJdo26jjdx7BwfbWtfEXgCn2xCuq2waCgYKAegSARISFQHGX2Mi1xc-irfTO7sTIUjCeM_Hpw0178"
        
        # id_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNjNWU0MTg0M2M1ZDUyZTY4ZWY1M2UyYmVjOTgxNDNkYTE0NDkwNWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiRmVyZGluYW5kIEFMTE9XQUtPVSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NLLWFRV3ZHUUUyYUpoNEMyQWNkNVpkQ25aNEx5TGtVNGZxbmZqVWdjeGN5QWNWNmc9czk2LWMiLCJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vd29ya2lubXVzaWMtMzBiMzciLCJhdWQiOiJ3b3JraW5tdXNpYy0zMGIzNyIsImF1dGhfdGltZSI6MTcyNTM0ODg4MiwidXNlcl9pZCI6IkpITTRLd0FzV0xUQ0JtUkc5b29hVVdHUmVFeTEiLCJzdWIiOiJKSE00S3dBc1dMVENCbVJHOW9vYVVXR1JlRXkxIiwiaWF0IjoxNzI1MzQ4ODgyLCJleHAiOjE3MjUzNTI0ODIsImVtYWlsIjoiZmFsbG93YWtvdUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMTU2OTIzMzY2NTMzNjg3NjAyNiJdLCJlbWFpbCI6WyJmYWxsb3dha291QGdtYWlsLmNvbSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.KO5B7MmTWTH4Z_9DW7LGvsr37s_Ja-jsspzqonkaTVOLLfpOfKdGFKG3bpt7zGJu4s87THaXT4eXyYz1mktKM_hp6fkO-tDmG2YaGjTwn1YaErKEOgS6hHBAHEGY0UbapcEA-vd792u252WI_jKNLW3d7V6iLDCI1Hu6yrTaepfG3D664dV8BwINus9dQ3CpWxigeExflmK6uYCyd9uQpZhWnQMOsCrsCUhmqT9otopMNTTJfLGxUhSCj4jwgcEK6hqfV90LbcVrAdGC0FXK0_8BB-p8cBF2NWqprpLlOhwk8ql7tHDbOilaBw3f6pRA9ALGkRgmI69pMRak0Z3yXQ"

        validate = Firebase_validation(request.data["access_token"])

        print("validate")
        print(validate)
        print("validate")

        if validate:
            # user = CustomUser.objects.filter(uid = validate["uid"]).first()
            user = CustomUser.objects.filter(email = validate["email"]).first()

            if user:
                
                data = {
                    "id": user.id,
                    "email": user.email,
                    "name": user.username,
                    "image": user.profilImg,
                    "type": "existing_user",
                    "provider": validate['provider']
                }

                return Response({"data": data,"message": "Login Successful" })

            else:

                # user = CustomUser(email = validate['email'],
                #                     name = validate['name'],

                #                     uid = validate['uid'],

                #                     image = validate['image']

                #                     )

                # user.save()

                # data = {
                #     "id": user.id,
                #     "email": user.email,
                #     "name": user.username,
                #     "image": user.profilImg,
                #     "type": "new_user",
                #     "provider": validate['provider']
                # }

                return Response({"data": validate,

                                "message": "User Created Successfully" })

        else:
            return Response({"message": "invalid token"})
    #    else:
    #         return Response({"message": "token not provided"})
                                            
                                            
class GoogleSocialAuthView(GenericAPIView):

    serializer_class = GoogleSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an idtoken as from google to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)


class FacebookSocialAuthView(GenericAPIView):

    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """

        POST with "auth_token"

        Send an access token as from facebook to get user information

        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = ((serializer.validated_data)['auth_token'])
        return Response(data, status=status.HTTP_200_OK)



