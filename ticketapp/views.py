from rest_framework import viewsets, permissions
from django.contrib.auth import get_user_model
from .models import Banner, Category, Event, Customer, Order, Ticket
from .serializers import CustomerSerializer, BannerSerializer, CategorySerializer, EventSerializer,  OrderSerializer, TicketSerializer 
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

Customer = get_user_model()

# Custom Permission
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.is_superuser:
            return True
        if hasattr(obj, "customer"):  # For Order
            return obj.customer == request.user
        if hasattr(obj, "order"):  # For Ticket
            return obj.order.customer == request.user
        return False

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Customer.objects.all() # admin can see all data
        return Customer.objects.filter(id=user.id)  # Customer sees only their own account
    def perform_update(self, serializer):
        user = self.request.user
        if not (user.is_staff or user.is_superuser) and serializer.instance != user.id:
            raise PermissionDenied("You cannot update another user's profile!!!")
        serializer.save()
    
from rest_framework.decorators import action#HLKKKKKKKKKKKKKKKKKKKKKKK
from rest_framework.response import Response#HLKKKKKKKKKKKKKKKKKKKKKKK

from rest_framework import status

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):#HLKKKKKKKKKKKKKKKKKKKKKKK
        serializer.save(order=Banner.objects.count() + 1)#HLKKKKKKKKKKKKKKKKKKKKKKK

    @action(detail=True, methods=['post'])#HLKKKKKKKKKKKKKKKKKKKKKKK
    def move_up(self, request, pk=None):#HLKKKKKKKKKKKKKKKKKKKKKKK
        banner = self.get_object()#HLKKKKKKKKKKKKKKKKKKKKKKK
        previous_banner = Banner.objects.filter(order__lt=banner.order).order_by('-order').first()#HLKKKKKKKKKKKKKKKKKKKKKKK
        if previous_banner:#HLKKKKKKKKKKKKKKKKKKKKKKK
            banner.order, previous_banner.order = previous_banner.order, banner.order#HLKKKKKKKKKKKKKKKKKKKKKKK
            banner.save()#HLKKKKKKKKKKKKKKKKKKKKKKK
            previous_banner.save()#HLKKKKKKKKKKKKKKKKKKKKKKK
        return Response({'status': 'success'})#HLKKKKKKKKKKKKKKKKKKKKKKK

    @action(detail=True, methods=['post'])#HLKKKKKKKKKKKKKKKKKKKKKKK
    def move_down(self, request, pk=None):#HLKKKKKKKKKKKKKKKKKKKKKKK
        banner = self.get_object()#HLKKKKKKKKKKKKKKKKKKKKKKK
        next_banner = Banner.objects.filter(order__gt=banner.order).order_by('order').first()#HLKKKKKKKKKKKKKKKKKKKKKKK
        if next_banner:#HLKKKKKKKKKKKKKKKKKKKKKKK
            banner.order, next_banner.order = next_banner.order, banner.order#HLKKKKKKKKKKKKKKKKKKKKKKK
            banner.save()#HLKKKKKKKKKKKKKKKKKKKKKKK
            next_banner.save()#HLKKKKKKKKKKKKKKKKKKKKKKK
        return Response({'status': 'success'})#HLKKKKKKKKKKKKKKKKKKKKKKK

    def destroy(self, request, *args, **kwargs):#HLKKKKKKKKKKKKKKKKKKKKKKK
        banner = self.get_object()#HLKKKKKKKKKKKKKKKKKKKKKKK
        deleted_order = banner.order#HLKKKKKKKKKKKKKKKKKKKKKKK
        response = super().destroy(request, *args, **kwargs)#HLKKKKKKKKKKKKKKKKKKKKKKK

        # Adjust orders of remaining banners
        remaining_banners = Banner.objects.filter(order__gt=deleted_order)#HLKKKKKKKKKKKKKKKKKKKKKKK
        for b in remaining_banners:#HLKKKKKKKKKKKKKKKKKKKKKKK
            b.order -= 1#HLKKKKKKKKKKKKKKKKKKKKKKK
            b.save()#HLKKKKKKKKKKKKKKKKKKKKKKK

        return response#HLKKKKKKKKKKKKKKKKKKKKKKK


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all() 
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

# Order : Only login customer or admin
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Order.objects.all() 
        return Order.objects.filter(customer=user) 
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

# Ticket : Only login customer or admin
class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Ticket.objects.all() 
        return Ticket.objects.filter(order__customer=user)

# Custom login view that accepts email instead of username
@api_view(['POST'])
@permission_classes([AllowAny])
def custom_login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not email or not password:
        return Response({'error': 'Email and password are required'}, status=400)
    
    try:
        user = Customer.objects.get(email=email)
    except Customer.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=401)
    
    if not user.check_password(password):
        return Response({'error': 'Invalid credentials'}, status=401)
    
    # Generate tokens
    refresh = RefreshToken.for_user(user)
    
    return Response({
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser
        }
    })
