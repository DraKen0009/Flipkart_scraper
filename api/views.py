import requests
from bs4 import BeautifulSoup
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers


# Create your views here.
class UserRegistrationAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'message': 'Account created successfully'
        }
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginAPIView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = serializers.UserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token), "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class UserAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user


class DataApiView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.DataSerializer

    def create(self, request, *args, **kwargs):
        url = request.data.get('url')
        if not url:
            raise ValidationError('Url field is required')

        if not url.startswith('http://') and not url.startswith('https://'):
            raise ValidationError('Incorrect url')

        respond = requests.get(url=url)
        content = respond.content
        soup = BeautifulSoup(content, 'html.parser')

        try:
            title = soup.find('span', class_='B_NuCI').text
            price = soup.find('div', class_='_30jeq3 _16Jk6d').text.replace(",", '')[1:]
            description = soup.find('div', class_='_2o-xpa').text
            num_media = len(soup.find_all('li', class_='_20Gt85 _1Y_A6W'))
            ratings = soup.find('div', class_='_2d4LTz').text
            num_rr = soup.find_all('div', class_='row _2afbiS')
            num_reviews = num_rr[1].find(name='span').text.split(" ")[0].replace(",", '')
            num_ratings = num_rr[0].find(name='span').text.split(" ")[0].replace(",", '')

        except:
            data = {'message': 'Incorrect url'}
            return Response(data=data,status=status.HTTP_400_BAD_REQUEST)

        scraped_data = {
            'user': request.user.id,
            'title': title,
            'price': price,
            'description': description,
            'num_media': num_media,
            'ratings': ratings,
            'num_reviews': num_reviews,
            'num_ratings': num_ratings,
            'url': url
        }

        serializer = self.get_serializer(data=scraped_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
