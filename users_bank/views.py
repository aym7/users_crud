from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.models import User

from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from .models import Customer
from .serializers import CustomerSerializer, UserSerializer
from .permissions import IsCreatorOrReadOnly


@api_view(["GET"])
def api_root(request, format=None):
    return Response({
        'admins': reverse('admin-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Use of generics pre-defined Generic views to have list and creation actions
class CustomerList(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Modify how the instance save is managed, handling any implicit information
    def perform_create(self, serializer):
        # Associates the user that created the Customer with it.
        serializer.save(owner=self.request.user)

class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Use of a generics view to automatically have the retrieve, update and destroy actions (GET, PUT, DELETE) on a specific customer.
    update and deletion are only allowed for the administrator who created the Customer.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # IsCreatorOrReadOnly allows modifications only for a Customer's creator
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]


