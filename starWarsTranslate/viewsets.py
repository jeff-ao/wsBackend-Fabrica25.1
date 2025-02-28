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

    def create(self, request):
        language = request.data.get('language')
        text = request.data.get('text')
        user_id = request.data.get('user_id')

        if not all([language, text, user_id]):
            return Response({"error": "language, text e user_id são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        translatedText = consultaAPI(language, text)

        translate_instance = Translates.objects.create(
            language=language,
            text=text,
            translatedText=translatedText,
            user_id=user,
        )

        serializer = self.get_serializer(translate_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

