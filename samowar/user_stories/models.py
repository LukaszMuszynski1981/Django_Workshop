from django.db import models
# Create your models here.


class Person(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=50)
    who_are_you = models.CharField(max_length=200, default='')
    image = models.ImageField(upload_to='project_pics', blank=True)


class Address(models.Model):
    city = models.CharField(max_length=30)
    pos_code = models.CharField(max_length=6)
    street = models.CharField(max_length=50)
    street_no = models.CharField(max_length=10)
    flat = models.CharField(max_length=10, default='')
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Phone(models.Model):
    types = (
        ('1', 'private'),
        ('2', 'office'),
    )
    phone = models.IntegerField()
    phone_type = models.CharField(max_length=1, choices=types, default=1)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Email(models.Model):
    types = (
        ('1', 'private'),
        ('2', 'office'),
    )
    email = models.CharField(max_length=100)
    email_type = models.CharField(max_length=1, choices=types, default=1)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)


class Group(models.Model):
    group_types = (
        ('1', 'Favourite'),
        ('2', 'Family'),

        ('3', 'Work'),
        ('4', 'Other'),
    )
    group_type = models.CharField(max_length=1, choices=group_types, default=1)
    person = models.ManyToManyField(Person)
