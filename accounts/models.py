from django.db import models
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.
class StaffUser(models.Model):
    DESIGNATION = [
    ('admin', 'Admin'),
    ('staff', 'Staff'),
    ]
    user = models.OneToOneField(to=User,null=True,on_delete=models.CASCADE)
    designation=models.CharField(max_length=200,choices=DESIGNATION)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)

    def __str__(self) -> str:
        if self.designation != None:
            return f"{self.user.first_name } {self.user.last_name} - {self.designation}"
        else:
            try:
                return f"{self.user.first_name } {self.user.last_name}"
            except:
                return super().__str__()
    @property
    def image_url(self):
        try:
            url = self.profile_picture.url
        except:
            url = ''

        return url