# Create your views here.
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import CustomUserUpdateSerializer, CustomUserCreateSerializer
from django.conf import settings
from firebase_admin import auth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from account.models import CustomUser
from account.serializers import CustomUserCreateSerializer
from firebase_admin import auth as firebase_auth

class GoogleLoginAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Authentifier un utilisateur avec le jeton d'identification Google",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id_token': openapi.Schema(type=openapi.TYPE_STRING, description='Jeton d\'identification Google')
            },
            required=['id_token']
        ),
        responses={
            200: openapi.Response(
                description="Authentification réussie",
                examples={
                    "application/json": {
                        "refresh": "string",
                        "access": "string"
                    }
                }
            ),
            400: openapi.Response(
                description="Requête invalide",
                examples={
                    "application/json": {
                        "detail": "Jeton d'identification requis."
                    }
                }
            ),
            404: openapi.Response(
                description="Utilisateur non trouvé",
                examples={
                    "application/json": {
                        "detail": "Utilisateur non trouvé."
                    }
                }
            ),
            500: openapi.Response(
                description="Erreur interne du serveur",
                examples={
                    "application/json": {
                        "detail": "Erreur lors de la vérification du jeton."
                    }
                }
            ),
        }
    )
    def post(self, request):
        id_token = request.data.get("id_token")

        if not id_token:
            return Response({"detail": "Jeton d'identification requis."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Vérifier le jeton avec Firebase Admin SDK
            decoded_token = firebase_auth.verify_id_token(id_token)
            email = decoded_token['email']
            google_user_id = decoded_token['uid']

            # Vérifier si l'utilisateur existe déjà dans la base de données
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                # Créer un nouvel utilisateur s'il n'existe pas
                user_data = {
                    "email": email,
                    "password": None,  # Vous pouvez générer un mot de passe aléatoire si nécessaire
                    "fullname": decoded_token.get('name', ''),
                }
                serializer = CustomUserCreateSerializer(data=user_data)
                if serializer.is_valid():
                    user = serializer.save()
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Générer un jeton JWT pour l'utilisateur
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except firebase_auth.InvalidIdTokenError:
            return Response({"detail": "Jeton d'identification invalide."}, status=status.HTTP_400_BAD_REQUEST)
        except firebase_auth.ExpiredIdTokenError:
            return Response({"detail": "Jeton d'identification expiré."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": "Erreur lors de la vérification du jeton."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpdateUserInfoView(generics.UpdateAPIView):
    serializer_class = CustomUserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user



class CustomUserCreateView(generics.CreateAPIView):
    serializer_class = CustomUserCreateSerializer
    permission_classes = [AllowAny]

