import random
import string
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
from .serializers import CartItemSerializer, StockSerializer, OrderSerializer
from .models import CartItem
from rest_framework.decorators import api_view, permission_classes
from .models import Stock, Order
from rest_framework.authtoken.models import Token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated


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
        token, _ = Token.objects.get_or_create(user=user)
        # print(token)
        # return Response(None, status=status.HTTP_200_OK) 
        return JsonResponse({'Auth_Token': token.key}, status=status.HTTP_200_OK)


class ListCartItems(generics.ListCreateAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

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

@api_view(['POST'])
def addStockItem(request):
    if request.method == 'POST':
        new_stock_data = JSONParser().parse(request)
        Med_title = new_stock_data['title']
        Med_price = new_stock_data['price']
        Med_cat = new_stock_data['category']
        if Med_title is not None and Med_price is not None and Med_cat is not None :
            items = Stock.objects.all()
            item = items.filter(title=Med_title)
            if(item is not None):
                serializer = None
                serializer = StockSerializer(data=new_stock_data)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse(serializer.data, status=status.HTTP_201_CREATED) 
                return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                return JsonResponse({'message': 'Item already exists!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'One of the fields is empty!'}, status=status.HTTP_204_NO_CONTENT)
        

class CategoryItems(generics.ListAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'title']


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def placeOrder(request):
    if request.method == 'POST':
        new_order = JSONParser().parse(request)
        if new_order is not None:
            serializer = None
            id = ''.join(random.choice(string.digits) for _ in range(6))
            print (new_order)
            print (id)
            # new_order(orderid)=id
            serializer = OrderSerializer(data=new_order, many=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
            return JsonResponse(serializer.errors, safe=False,  status=status.HTTP_400_BAD_REQUEST)
        else:
            return JsonResponse({'message': 'No orders found!'}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthenticated])
class ViewOrders(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id']