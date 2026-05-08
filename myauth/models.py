import profile
from profile import Profile

from django.contrib.auth.models import User
from django.db import models


def avatar_images_directory_path(instance: 'Profile', filename: str) -> str:
    return 'avatars/{username}/{filename}'.format(
        # pk=instance.user.pk,
        username=instance.user.username,
        filename=filename
    )


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=False)
    agreement_accepted = models.BooleanField(default=False)
    avatar = models.ImageField(null=True, blank=True, upload_to=avatar_images_directory_path)
    # def __str__(self) -> str:
    #     return f'Profile(pk={self.pk}, name={self.user!r})'
# class ProfileImages(models.Model):
#     profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='images')
#     image = models.ImageField(upload_to=profile_avatar_directory_path)
#     description = models.CharField(max_length=200, null=False, blank=True)
