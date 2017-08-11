from django.db import models
from django.contrib.auth.models import AbstractUser
import hashlib
import urllib
import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class UserProfile(models.Model):
    BRANCH_CHOICES=(
        ('0','Bio-Chemical Engg.'),
        ('1', 'Bio-Medical Engg'),
        ('2', 'Ceramic Engg.'),
        ('3', 'Chemical Engg.'),
        ('4', 'Chemistry'),
        ('5', 'Civil Engg.'),
        ('6', 'Computer Engg.'),
        ('7', 'Electrical Engg.'),
        ('8', 'Electronic Engg.'),
        ('9', 'Material Sc. and Tech.'),
        ('10', 'Mathematical Sciences'),
        ('11', 'Mechanical Engg.'),
        ('12', 'Metallurgical Engg.'),
        ('13', 'Mining Engg.'),
        ('14', 'Pharmaceutical Engineering & Technology'),
        ('15', 'Physics'),

    )
    YEAR_CHOICES=(
        ('0','1st'),
        ('1','2nd'),
        ('2','3rd'),
        ('3','4th'),
        ('4','5th'),

    )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='', blank=True)
    phone = models.CharField(max_length=20, blank=True, default='')
    city = models.CharField(max_length=100, default='', blank=True)
    branch = models.CharField(max_length=100, default='', blank=True,choices=BRANCH_CHOICES)
    year = models.CharField(max_length=100, default='', blank=True,choices=YEAR_CHOICES)


    def get_picture(self):
        no_picture = '/static/img/1.jpg'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' + \
                       self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + '/profile_pictures/' + \
                          self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                )
                return gravatar_url
        except Exception:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username



def create_profile(sender, **kwargs):
    user = kwargs["instance"]

    if kwargs["created"]:
        user_profile = UserProfile(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)
