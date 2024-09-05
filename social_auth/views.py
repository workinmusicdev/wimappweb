import os
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from accountapp.models import CustomUser
from accountapp.serializers import CustomUserSerializer
from licenceapp.serializers import LicenceSerializer
from social_auth.serializers import GoogleSocialAuthSerializer, FacebookSocialAuthSerializer, SocialAuthSerializer
from social_auth.utils import generate_username, validate_firebase_token
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken


class SocialSignupAPIView(GenericAPIView):
    """
    API pour l'inscription et la connexion via les réseaux sociaux.
    """
    permission_classes = [AllowAny]
    serializer_class = SocialAuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        access_token = serializer.validated_data['access_token']
        provider = serializer.validated_data['provider']
        
        validate = validate_firebase_token(access_token)
        
        if validate:
            print(validate)
            email = validate.get('email')
            name = validate.get('name') or email.split('@')[0]
            provider = validate.get('provider')
            image = validate.get('image')
            
            try:
                user = CustomUser.objects.get(email=email)
                print(user)
                print(user.auth_provider)
                print(provider)
                print(user.password)

                if user.auth_provider != provider:
                    raise AuthenticationFailed(
                        detail=f'Veuillez vous connecter via {user.auth_provider}.')

                # Authentifier l'utilisateur avec un mot de passe secret pour les utilisateurs sociaux
                # user = authenticate(email=email, password=os.environ.get('SOCIAL_SECRET'))
                print('-------------')
                print(user)
                print('-------------')
                if user:
                    refresh = RefreshToken.for_user(user)
                    licences = user.licences.all()
                    serializer = LicenceSerializer(licences, many=True)
                    print('-------------+++++')
                    print(refresh)
                    print(refresh.access_token)
                    print('-------------+++++')
                    user_data = CustomUserSerializer(user).data

                    return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        # 'tokens': user.tokens(),
                        'user': user_data,
                        'licences': serializer.data
                    }, status=status.HTTP_200_OK)
                else:
                    raise AuthenticationFailed('Échec de l\'authentification.')
            
            except CustomUser.DoesNotExist:
                # Créer un nouvel utilisateur
                print("Créer un nouvel utilisateur")
                username = generate_username(name)
                user = CustomUser.objects.create_user(
                    email=email,
                    username=username,
                    password=os.environ.get('SOCIAL_SECRET'),
                    auth_provider=provider,
                    is_verified=True,
                    profilImg=image
                )
                user.save()
                print(user.id)

                # Authentifier le nouvel utilisateur
                # user = authenticate(email=email, password=os.environ.get('SOCIAL_SECRET'))
                print(user)
                refresh = RefreshToken.for_user(user)
                licences = user.licences.all()
                serializer = LicenceSerializer(licences, many=True)

                return Response({
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'user': {
                            'id': user.id,
                            'email': user.email,
                            'isAuto': user.is_auto,
                        },
                        'licences': serializer.data
                    }, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Token invalide ou expiré.'}, status=status.HTTP_400_BAD_REQUEST)


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
