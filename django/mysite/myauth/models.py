from django.db import models
from django.contrib.auth.models import User



def profile_avatar_directory_path(instance:"User",filename:str)->str:
    return 'about-me/users_{pk}/avatar/{filename}'.format(
        pk=instance.pk,
        filename=filename,
    )

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500,blank=True) #может быть пустой
    agreement_accepted = models.BooleanField(default=False)

    avatar = models.ImageField(null=True,blank=True,upload_to=profile_avatar_directory_path)
