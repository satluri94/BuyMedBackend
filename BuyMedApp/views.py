from django.shortcuts import render

from .models import User
from .serializers import RegisterSerializer
from .serializers import LoginSerializer
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from . import serializers
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework import viewsets
from .serializers import CartItemSerializer
from .models import CartItem
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

# Create your views here.

class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        #Check login is successful or not
        # token = Token.objects.create(user=...)
        return Response(None, status=status.HTTP_200_OK) 
        # return JsonResponse({'Auth_Token': token.key}, status=status.HTTP_200_OK)


class ListCartItems(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    
# def get_cartItems(request):
    # cartItems = CartItem.objects.all()    # 
    # Serialize the model instances into a JSON string
    # serialized_objects = CartItemSerializer.serialize('json', cartItems)
    # Return a JSON response with the serialized objects
    # return JsonResponse(serialized_objects, safe=False)

@api_view(['POST'])
def addCartItem(request):
    if request.method == 'POST':
        new_cart_data = JSONParser().parse(request)
        product_title = new_cart_data['title']
        product_price = new_cart_data['price']
        if product_title is not None and product_price is not None:
            items = CartItem.objects.all()
            item = items.filter(title=product_title)
            if(item is not None):
                serializer = None
                serializer = CartItemSerializer(data=new_cart_data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                return JsonResponse({'message': 'Product already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'One of the fields is empty!'}, status=status.HTTP_204_NO_CONTENT)

