from django.shortcuts import get_object_or_404
from rest_framework.decorators import  api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView
from .models import Product,Collection
from django.db.models import Count
from .serializers import ProductSerializer,CollectionSerializer
from rest_framework import status


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all()
    serializer_class = ProductSerializer

    def get_serializer_context(self):
        return {'request':self.request}
    

class ProductDetail(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def delete(self,request,pk ):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({'error': 'Product cannot be deleted because it is associated with an orderitem.'})
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CollectionList(ListCreateAPIView):
     queryset = Collection.objects.annotate(products_count=Count('products')).all()
     serializer_class = CollectionSerializer
        
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(
            products_count=Count('products'))
    serializer_class = CollectionSerializer

    def delete(self,request,pk):
        collection = get_object_or_404(Collection,pk=pk)
        if collection.products.count() > 0:
            return Response({"error":'Collection cannot be deleted because it includes one or more products.'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)