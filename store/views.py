from django.shortcuts import get_object_or_404
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import Product,Collection
from django.db.models import Count
from .serializers import ProductSerializer,CollectionSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    
    def delete(self,request,pk ):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an orderitem.'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
  
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def delete(self,request,pk):
        collection = get_object_or_404(Collection,pk=pk)
        if collection.products.count() > 0:
            return Response({"error":'Collection cannot be deleted because it includes one or more products.'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


   

    