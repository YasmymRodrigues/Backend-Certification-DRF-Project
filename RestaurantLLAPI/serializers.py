from rest_framework import serializers
from .models import MenuItem
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .models import MenuItem, Order, OrderItem, Cart
from decimal import Decimal
from .models import Category

#import bleach

# @api_view()
# def menu_items(request):
#     items = MenuItem.objects.all()
#     return Response(items.values())


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    #id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)
    #stock = serializers.IntegerField(source = 'inventory')
    #price_after_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    featured = serializers.BooleanField()
    category = CategorySerializer(read_only = True)
    category_id = serializers.IntegerField(write_only = True)
    #category = serializers.StringRelatedField(read_only=True)
    #category = CategorySerializer(read_only = True)


    class Meta:
            model = MenuItem
            fields = ['id','title', 'price', 'featured', 'category', 'category_id']
            #depth = 1
            extra_kwargs={
                'price': {'min_value': 2},
                #'stock': {'source':'inventory', 'min_value' : 0}
            }


#     def calculate_tax(self, product:MenuItem):
#         return product.price * Decimal(1.1)


class OrderSerializer(serializers.ModelSerializer):
     status = serializers.BooleanField()
     #category = serializers.StringRelatedField(read_only=True)
     total = serializers.DecimalField(max_digits=6, decimal_places=2)
     
     class Meta:
          model = Order
          fields = ['user', 'delivery_crew', 'status', 'total', 'date']
          extra_kwargs = {
                'status': {'delivered': False}
           }

    
class OrderItemSerializer(serializers.ModelSerializer):    
    order = serializers.StringRelatedField(read_only=True)
    menuitem = serializers.StringRelatedField(read_only=True)
    quantity = serializers.IntegerField()
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price = serializers.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
         model = OrderItem
         fields =['order', 'menuitem', 'quantity', 'unit_price', 'price']
         #extra_kwargs = {}

class CartSerializer(serializers.ModelSerializer):
    menuitem_name = serializers.CharField(source='menuitem.title', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    class Meta:
         model = Cart
         fields = ['id', 'user', 'user_name', 'menuitem', 'menuitem_name', 'quantity', 'unit_price', 'price']
