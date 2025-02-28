from rest_framework import serializers
from .models import Users, Translates

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
        
class TranslatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Translates
        fields = '__all__'