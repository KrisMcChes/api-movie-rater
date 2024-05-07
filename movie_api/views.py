from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

from .models import Movie, Rating
from .serializers import MovieSerializer, RatingSerializer, UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny, ]
        else:
            permission_classes = [IsAuthenticated, ]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if 'password' in serializer.validated_data:
                user.set_password(serializer.validated_data['password'])
                user.save()

            token, created = Token.objects.get_or_create(user=user)

            data = serializer.data
            data['token'] = token.key

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    authentication_classes = [TokenAuthentication, ] 
    permission_classes = [AllowAny, ]

    # this is a custom action with 
    # detail=True - this action will be called on a particular movie instance
    # url: https://localhost:8000/api/movies/<id>/rate_movie/
    @action(detail=True, methods=['POST'])
    def rate_movie(self, request, pk=None):
        if 'stars' in request.data:
            
            movie = Movie.objects.get(id=pk)
            stars = request.data['stars']
            # the default way to get user but we can't get user from Postman request because its' anonymous
            user = request.user
            # so we get user from request.data
            # user = User.objects.get(id=request.data['user'])
            # this can be fixed by Authentication classes
            
            print(pk, movie, user, stars)

            try:
                rating = Rating.objects.get(user=user.id, movie=movie.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating updated', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            except:
                rating = Rating.objects.create(user=user, movie=movie, stars=stars)
                serializer = RatingSerializer(rating, many=False)
                response = {'message': 'Rating created', 'result': serializer.data}
                return Response(response, status=status.HTTP_200_OK)
            
        else:
            response = {'message': 'Please provide movie rating with stars'}
            return Response(response, status = status.HTTP_400_BAD_REQUEST)

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication, ] 
    permission_classes = [IsAuthenticated, ]

    # One of the ways to override default methods in ModelViewSet to prevent user from accessing different methods
    # Override the default update method from ModelViewSet to prevent updating a movie
    def update(self, request, *args, **kwargs):
        response = {'message': 'You can\'t update a rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
    
    # Override the default create method from ModelViewSet to prevent creating a movie
    def create(self, request, *args, **kwargs):
        response = {'message': 'You can\'t update a rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)