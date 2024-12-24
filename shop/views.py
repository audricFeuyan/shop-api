from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer, ProductSerializer, ArticleSerializer

class CategoryViewset(ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.filter(active=True)
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return self.detail_serializer_class
        return super().get_serializer_class()

    
class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        query_set = Product.objects.filter(active=True)
        category_id = self.request.GET.get('category_id')

        if category_id is not None:
            query_set = query_set.filter(category_id=category_id)

        return query_set
    

class ArticleViewset(ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        query_set = Article.objects.filter(active=True)
        product_id = self.request.GET.get('product_id')

        if product_id is not None:
            query_set = query_set.filter(product_id=product_id)

        return query_set
