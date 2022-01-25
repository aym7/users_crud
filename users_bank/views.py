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
    """Homepage to our application. Present our two main entry points.
    """
    return Response({
        'admins': reverse('admin-list', request=request, format=format),
        'users': reverse('user-list', request=request, format=format),
    })


class UserList(generics.ListAPIView):
    """Provides the List action
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    """Provides the Retrieve (GET) action on a specific user/admin
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CustomerList(generics.ListCreateAPIView):
    """ Use of a generics view to automatically have list and create actions.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """Associates the user that created the Customer with it.
        Modify how the instance save is managed, handling any implicit information
        """
        serializer.save(creator=self.request.user)


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    """ Use of a generics view to automatically have actions on a specific customer.
    actions available are: retrieve, update and destroy (GET, PUT, DELETE).
    update and deletion are only allowed for the administrator who created the Customer.
    """
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # IsCreatorOrReadOnly allows modifications only for a Customer's creator
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]
