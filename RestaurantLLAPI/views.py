from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem, Order, OrderItem, Cart, Category
from .serializers import MenuItemSerializer, OrderSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes, throttle_classes
from rest_framework.throttling import AnonRateThrottle #limite the amount of calls per a certain time
from rest_framework.throttling import UserRateThrottle
from .throttles import FiveCallsPerMinute
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User, Group


# Create your views here.
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()    
    serializer_class = MenuItemSerializer

class SingleMenuItem(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer


@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all() #for a single call
        category_name = request.query_params.get('category') #filter
        to_price = request.query_params.get('to_price') #filter
        search = request.query_params.get('search') #search
        perpage = request.query_params.get('perpage', default=10) #pagination
        page = request.query_params.get('page', default=1)#pagination
        if category_name: #filter
            items = items.filter(category_title=category_name)#filter
        if to_price: #filter
            items = items.filter(price = to_price) #filter
        if search:
            items = items.filter(title__icontains = search)
        paginator = Paginator(items, per_page=perpage)
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many = True) #many = convert with Json
        return Response(serialized_item.data)
    elif request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)

@api_view(['GET'])
def single_item(request, pk):    
    if request:      
        item = get_object_or_404(MenuItem, pk=pk)
        serialized_item = MenuItemSerializer(item)
        return Response(serialized_item.data)


@api_view(['GET', 'POST'])
def orders(request):
    if request.method == 'GET': 
        items = Order.objects.all()    
        serialized_items = OrderSerializer(data = list(items), many = True)
        serialized_items.is_valid(raise_exception=True)
        return Response(serialized_items.data)
    elif request.method == "POST":
        serialized_items = OrderSerializer(data=request.data)
        serialized_items.is_valid(raise_exception=True)
        serialized_items.save()
        return Response(serialized_items.data)



@api_view
def orders_item(request, pk):
    if request:
        item = get_object_or_404(Order, pk = pk)
        serializer_item = OrderSerializer(item)
        return Response(serializer_item.data)



@api_view(['GET', 'POST'])
def cart(request,pk):
    items = Cart.objects.all()
    if request.method == 'GET':
        carts = Cart.objects.filter(user=str(id))
        serialized_carts = CartSerializer(carts, many=True)
        return Response(serialized_carts)



@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})


@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([FiveCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message":"message for the logged in users only"})

#User registration system
@api_view()
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name="Manager")
        if request.method =='POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({"message":"ok"})
    return Response({"message":"erro"}), status.HTTP_400_BAD_REQUEST

