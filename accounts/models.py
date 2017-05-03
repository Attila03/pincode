from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
STATE_LIST = (
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chattisgarh', 'Goa',
    'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka',
    'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
    'Orissa', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Tripura', 'Uttaranchal', 'Uttar Pradesh',
    'West Bengal', 'Andaman and Nicobar Islands', 'Chandigarh', 'Dadar and Nagar Haveli', 'Daman and Diu',
    'Delhi', 'Lakshadeep', 'Pondicherry'
)

class Address(models.Model):
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    locality = models.CharField(max_length=150)
    apartment = models.CharField(max_length=50, verbose_name='Flat No./Bldg. No., Apartment')
    pincode = models.IntegerField(blank=True)

    def __str__(self):
        return "{}, {}, {}, {}, India.".format(self.apartment, self.locality, self.city, self.state)


class Profile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    address = models.OneToOneField(Address, blank=True, null=True)


    def __str__(self):
        return "{}".format(self.user.username)

@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

