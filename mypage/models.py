from django.db import models
from accounts.models import User

# Create your models here.
class Test(models.Model):
    user = models.ForeignKey("accounts.User", null=True, on_delete=models.CASCADE)
    question1 = models.BooleanField(default=False)
    question2 = models.BooleanField(default=False)
    question3 = models.BooleanField(default=False)
    question4 = models.BooleanField(default=False)
    question5 = models.BooleanField(default=False)
    #profile_number = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.user}'