from django.shortcuts import get_object_or_404
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import OrderItem, Product,Collection
from django.db.models import Count
from .serializers import ProductSerializer,CollectionSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    
    def destroy(self,request,*args,**kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an orderitem.'})

        return super().destroy(request,*args,**kwargs)

    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self,request,*args,**kwargs):
        if collection.products.count() > 0:
            return Response({"error":'Collection cannot be deleted because it includes one or more products.'})
        
        return super().destroy(self,request,*args,**kwargs)


   

    