from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

#Create a cipher model
class Ciphers(models.Model):
    user = models.ForeignKey(
        User, related_name="ciphers",
        on_delete = models.DO_NOTHING
    )

    body = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return(
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body}..."
        )


# Create User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Cascade is used to delete everything underneath
    follows = models.ManyToManyField("self",
                                     related_name="Followed_by",
                                     # Followed by is used to show who follows who when visiting account
                                     symmetrical=False,  # Users dont HAVE to always follow each other.
                                     blank=True)  # You dont have to always follow someone

    date_modified = models.DateTimeField(User, auto_now=True)

    def __str__(self):
        return self.user.username


# Create your models here.

# Create profile automatically when user signs up
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        # Have user follow himself to see his ciphers in homepage
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


post_save.connect(create_profile, sender=User)
