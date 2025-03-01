from django.db import models

# Create your models here.

class Users(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}, {self.email}, {self.createdAt}"
    
class Translates(models.Model):
    language = models.CharField(max_length=255)
    text = models.TextField()
    translatedText = models.TextField(null=True,blank=True)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__ (self):
        return f"language: {self.language}, text: {self.text}, translated text: {self.translatedText}, created at: {self.createdAt}, user id: {self.user_id}"
    