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
        
        if language not in {"yoda", "sith", "mandalorian", "huttese", "gungan", "cheunh"}:
            return Response({"error": "Linguagem não suportada"}, status=status.HTTP_400_BAD_REQUEST)
       
        if not isinstance(text, str) or len(text) > 1000:
            return Response({"error": "Texto invalido"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not isinstance(user_id, int):
            return Response({"error": "Id do usuario invalido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({"error": "Usuario não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        translatedText = consultaAPI(language, text)

        translate_instance = Translates.objects.create(
            language=language,
            text=text,
            translatedText=translatedText,
            user_id=user,
        )

        serializer = self.get_serializer(translate_instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        try:
            translate = Translates.objects.get(id=pk)
        except Translates.DoesNotExist:
            return Response({"error": "Tradução não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(translate)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        
        language = request.data.get('language')
        text = request.data.get('text')
        user_id = request.data.get('user_id')

        if not all([language, text, user_id]):
            return Response({"error": "language, text e user_id são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Id do usuário inválido"}, status=status.HTTP_400_BAD_REQUEST)

        if language not in {"yoda", "sith", "mandalorian", "huttese", "gungan", "cheunh"}:
            return Response({"error": "Linguagem não suportada"}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(text, str) or len(text) > 1000:
            return Response({"error": "Texto inválido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            translate = Translates.objects.get(id=pk)
        except Translates.DoesNotExist:
            return Response({"error": "Tradução não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        try:
            Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return Response({"error": "Usuário não encontrado"}, status=status.HTTP_404_NOT_FOUND)

        if user_id != translate.user_id.id:
            return Response({"error": "Você não tem permissão para editar essa tradução"}, status=status.HTTP_403_FORBIDDEN)

        translatedText = consultaAPI(language, text)

        translate.language = language
        translate.text = text
        translate.translatedText = translatedText
        translate.save()

        serializer = self.get_serializer(translate)
        return Response(serializer.data, status=status.HTTP_200_OK)
        #exemple of request
        #{
        #    "language": "yoda","text": "I am a Jedi like my father before me","user_id": 1
        #}
    
    def partial_update(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        language = request.data.get('language')
        text = request.data.get('text')
        user_id = request.data.get('user_id')

        try:
            translate = Translates.objects.get(id=pk)
        except Translates.DoesNotExist:
            return Response({"error": "Tradução não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        if user_id:
            try:
                user_id = int(user_id)
            except ValueError:
                return Response({"error": "Id do usuário inválido"}, status=status.HTTP_400_BAD_REQUEST)

            if user_id != translate.user_id.id:
                return Response({"error": "Você não tem permissão para editar essa tradução"}, status=status.HTTP_403_FORBIDDEN)

        if language and language not in {"yoda", "sith", "mandalorian", "huttese", "gungan", "cheunh"}:
            return Response({"error": "Linguagem não suportada"}, status=status.HTTP_400_BAD_REQUEST)

        if text and (not isinstance(text, str) or len(text) > 1000):
            return Response({"error": "Texto inválido"}, status=status.HTTP_400_BAD_REQUEST)

        return super().partial_update(request, *args, **kwargs)

    
    def destroy(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        user_id = request.query_params.get('user_id')

        if user_id is None:
            return Response({"error": "user_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_id = int(user_id)
        except ValueError:
            return Response({"error": "Id do usuário inválido"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            translate = Translates.objects.get(id=pk)
        except Translates.DoesNotExist:
            return Response({"error": "Tradução não encontrada"}, status=status.HTTP_404_NOT_FOUND)

        if user_id != translate.user_id.id:
            return Response({"error": "Você não tem permissão para deletar essa tradução"}, status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)

