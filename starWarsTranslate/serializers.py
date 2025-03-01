from rest_framework import serializers
from .models import Users, Translates

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'email', 'createdAt', 'updatedAt']
        
class TranslatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translates
        fields = '__all__'
        read_only_fields = ['translatedText']