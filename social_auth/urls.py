from django.urls import path

from social_auth.views import GoogleSocialAuthView, FacebookSocialAuthView
from .views import SocialSignupAPIView

urlpatterns = [
    path('google/', GoogleSocialAuthView.as_view()),
    path('facebook/', FacebookSocialAuthView.as_view()),
    path('socialSignup/', SocialSignupAPIView.as_view(), name= "social-signup"),
]