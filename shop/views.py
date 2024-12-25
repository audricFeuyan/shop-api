from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from shop.models import Category, Product, Article
from shop.serializers import CategoryDetailSerializer, CategoryListSerializer, ProductSerializer, ArticleSerializer


class MultipleSerializerMixin:
    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        
        return super().get_serializer_class()
    
class CategoryViewset(MultipleSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

    def get_queryset(self):
        return Category.objects.filter(active=True)
    
class AdminCategoryViewset(MultipleSerializerMixin, ModelViewSet):
    serializer_class = CategoryListSerializer
    detail_serializer_class = CategoryDetailSerializer

    def get_queryset(self):
        return Category.objects.all()

    
class ProductViewset(ModelViewSet):
    serializer_class = ProductSerializer

    @action(detail=True, methods=['post'])
    def disable(self, request, pk):
        self.get_object().disable()
        return Response()

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
    
class AdminArticleViewset(ModelViewSet):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        query_set = Article.objects.all()
        product_id = self.request.GET.get('product_id')

        if product_id is not None:
            query_set = query_set.filter(product_id=product_id)

        return query_set
    
        
