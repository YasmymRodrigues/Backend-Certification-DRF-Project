from django.shortcuts import render
from rest_framework import generics
from .models import MenuItem
from .serializers import MenuItemSerializer
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
            items = items.filter(title__startswith = search)
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

@api_view
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)



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

