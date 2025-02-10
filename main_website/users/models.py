from django.db import models
from datetime import datetime
import os, random
from django.utils import timezone
from django.utils.html import mark_safe

now = timezone.now()
# Create your models here.

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890'
    randomstr = ''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()
    
    return 'profile_pic/{year}-{month}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance,
    basename=basefilename, randomstring=randomstr, ext=file_extension, year=_now.strftime('%Y'), month=_now.strftime('%m'), day=_now.strftime('%d'))
