from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class usermanager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        if username is None:
            raise TypeError("users should have a username")
        if email is None:
            raise TypeError("users  should have a email")
        user = self.model(username=username, email=self.normalize_email(email), **extra_fields)
        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_field):

        extra_field.setdefault('is_staff', True)
        extra_field.setdefault('is_superuser', True)
        extra_field.setdefault('is_active', True)
        if username is None:
            raise TypeError("users should have a username")

        if email is None:
            raise TypeError("users  should have a email")

        if extra_field.get('is_staff') is not True:
            raise ValueError('is_staff is not')
        if extra_field.get('is_superuser') is not True:
            raise ValueError('is_sueruser is not')
        if extra_field.get('is_active') is not True:
            raise ValueError('is_active is not')
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    username = models.CharField(max_length=34, db_index=True)
    email = models.EmailField(max_length=34, unique=True, db_index=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = usermanager()

    def __str__(self):
        return self.email


class Category(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=34)
    time = models.DateTimeField(auto_now_add=True)


class Book(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=34)
    title = models.CharField(max_length=34)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="book")
    descriptions = models.CharField(max_length=200)
    prize = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    book_buy = models.IntegerField(default=0)


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="orderbook")
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now_add=True)
    pincode = models.CharField(max_length=4)

    def save(self, *args, **kwargs):
        book = Book.objects.filter(id=self.book.id).first()
        book.book_buy += 1
        book.save()
        self.book.book_buy += 1
        super(Order, self).save(*args, **kwargs)
