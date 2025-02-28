from rest_framework import viewsets, status
from rest_framework.response import Response
import requests
from .models import Users, Translates
from .serializers import UserSerializer, TranslatesSerializer

def consultaAPI(language, text):
    url = f"https://api.funtranslations.com/translate/{language}/?text={text}"
    response = requests.get(url)
    return response.json()["contents"]["translated"]

class UserViewSets(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UserSerializer
    
    
class TranslatesViewSets(viewsets.ModelViewSet):
    queryset = Translates.objects.all()
    serializer_class = TranslatesSerializer