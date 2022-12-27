from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.utils.safestring import mark_safe


class UserProfile(models.Model):
    MISSION = (

        ('PAIE', 'Responsable_paiement'),
        ('CDE', 'Responsable_commande'),
        ('DEUX', 'Les_deux'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nom_societe = models.CharField(max_length=100)
    mission = models.CharField(max_length=10, choices=MISSION, blank=True, null=True)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')
    created = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated = models.DateTimeField(auto_now=True, blank=True,null=True)



    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class ProfilePro(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    raison_social = models.CharField(max_length=30, blank=True)
    compte = models.CharField(max_length=6, blank=True )
    ville = models.CharField(max_length=50, blank=True)
    catalog = models.BooleanField(default=False)
    releve = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated = models.DateTimeField(auto_now=True, blank=True,null=True)


    def __str__(self):
        return self.raison_social


class Releve(models.Model):
    compte = models.ForeignKey(User, on_delete=models.CASCADE)
    date_fac = models.DateField()
    ref_fac = models.CharField(max_length=50)
    mnt_ttc = models.DecimalField(max_digits=10, decimal_places=2)
    mnt_regler = models.DecimalField(max_digits=10, decimal_places=2)
    solde = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return str(self.compte)
