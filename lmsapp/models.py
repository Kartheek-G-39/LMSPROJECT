from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _
from django.contrib.auth.models import UserManager,AbstractBaseUser,PermissionsMixin
# Create your models here.
class users(UserManager):
    def _create_user(self,email,password,**extrafields):
        if not email:
            raise ValueError("Please enter an valid e-mail id")
        email = self.normalize_email(email)
        user = self.model(email=email,**extrafields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password=None,**extrafields):
        extrafields.setdefault("is_staff",False)
        extrafields.setdefault("is_superuser",False)
        return self._create_user(email,password,**extrafields)
    def update_password(self,email,password):
        user = self.get(email=email)
        user.set_password(password)
        user.save(using=self._db)
    def create_superuser(self,email, password= None,**extrafields):
        extrafields.setdefault("is_staff",True)
        extrafields.setdefault("is_superuser",True)
        return self._create_user(email,password,**extrafields)
    
class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(primary_key=True,blank=True,default='',unique=True)

    is_active=models.BooleanField(default=True)
    is_superuser=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)

    date_field=models.DateTimeField(default=timezone.now)
    last_login=models.DateField(blank=True,null=True)

    objects=users()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

class userdata(models.Model):
    usermail = models.ForeignKey(User, verbose_name=_("User Infromation"), on_delete=models.CASCADE)
    GENDER_CHOICES = (
        ('M', 'Homme'),
        ('F', 'Femme'),
    )
    name = models.CharField(_("Name"), max_length=50)
    rollnumber =models.CharField(_("RollNo."), max_length=10,unique=True)
    gender = models.CharField(_("Gender"), max_length=1,choices=GENDER_CHOICES)
    branch = models.CharField(_("Branch"), max_length=10)
    section = models.CharField(_("Section"), max_length=50)
    libraryid = models.CharField(_("Library ID"), max_length=50)