from rest_framework import serializers
from .models import MenuItem
from rest_framework.response import Response 
from rest_framework.decorators import api_view
from .models import MenuItem
from decimal import Decimal
from .models import Category
#import bleach

@api_view()
def menu_items(request):
    items = MenuItem.objects.all()
    return Response(items.values())


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField
    price = serializers.DecimalField(max_digits=3, decimal_places=2)
    #stock = serializers.IntegerField(source = 'inventory')
    #price_after_tax = serializers.SerializerMethodField(method_name= 'calculate_tax')
    featured = serializers.BooleanField
    category = serializers.StringRelatedField(read_only=True)
    #category = CategorySerializer(read_only = True)


    class Meta:
            model = MenuItem
            fields = ['id', 'title', 'price', 'featured' ,'category']
            depth = 1
            extra_kwargs={
                'price': {'min_value': 2},
                #'stock': {'source':'inventory', 'min_value' : 0}
            }


    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)