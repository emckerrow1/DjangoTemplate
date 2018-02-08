# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# third-party
import uuid

def genid(id_label):
    return id_label+"--"+str(uuid.uuid4())

# Create your models here.
class UserProfile(models.Model):
    stix_id = models.CharField(max_length=100, default=genid('identity'), unique=True)
    user = models.OneToOneField(User)
    image_url = models.CharField(max_length=75, default="Profile_Pic_default.png")
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
