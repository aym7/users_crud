from django.db import models
from django.urls import reverse

# Create your models here.
class Customer(models.Model):
    # TODO: Check (iban = only caps, letters and numbers)
    # blank=False means the field is rendered as required
    # null=True means that the field can be empty in the DB    
    first_name = models.CharField(max_length = 120)
    last_name = models.CharField(max_length = 120)
    iban = models.CharField(max_length = 50)

    # creator represents the Admin who created the Customer's instance.
    # Useful to see who can update the 
    creator = models.ForeignKey('auth.User',
        related_name='customers', on_delete=models.CASCADE)



