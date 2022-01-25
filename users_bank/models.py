from django.db import models


class Customer(models.Model):
    """Our main model.
    Called 'Customer' in order to avoid conflict with django.db.auth's User model.
    """
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    iban = models.CharField(max_length=50)

    # creator represents the Admin who created the Customer's instance.
    # Useful to see who can update/delete the instance
    creator = models.ForeignKey('auth.User',
                                related_name='customers', on_delete=models.CASCADE)
