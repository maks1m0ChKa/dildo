from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'id': ['exact'],
        'title': ['exact']
    }


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    filterset_fields = {
        'id': ['exact'],
        'price': ['exact', 'gt', 'lt', 'gte', 'lte'],
        'title': ['exact'],
        'category': ['exact']
    }
    ordering_fields = ['title', 'price']
    ordering = ['title']
    search_fields = ['title']

class UserManager(BaseUserManager):

    use_in_migration = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is Required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff')is not True:
            raise ValueError('Superuser must have is_staff = True')
        if extra_fields.get('is_superuser')is not True:
            raise ValueError('Superuser must have is_staff = True')
        
        return self.create_user(email,password, **extra_fields)
    
    class UserData(AbstractUser):
        username = None
        name = models.CharField(max)