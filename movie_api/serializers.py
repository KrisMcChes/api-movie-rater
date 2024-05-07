from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import Movie, Rating
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        # this line will protect the password field from being displayed in the API
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        # add functions from the model to serializer so that we can use them in the API
        # function no_of_ratings will automatically retrieve the number of ratings for a movie and display it in the API when we pass it to serializer
        fields = ('id', 'title', 'description', 'no_of_ratings', 'avg_rating')
        
class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id', 'movie', 'user', 'stars')