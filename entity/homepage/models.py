from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    dob = models.DateTimeField('birthdate')
    date_created = models.DateTimeField('date created')
    def __str__(self):
        return self.username
    
class Job(models.Model):
    name = models.CharField(max_length=200) 
    description = models.TextField(max_length=600)
    price = models.DecimalField(max_digits = 8, decimal_places = 2) #arbitrary values!
    location = models.CharField(max_length=200)
    taken = models.BooleanField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE) #foreign key for owner
    cleaner = models.ForeignKey(User, related_name="cleaner_job",null=True) 
    date_created = models.DateTimeField('date created')
    def __str__(self):
        return self.name
    
class Authenticator(models.Model):
    authenticator = models.CharField(max_length=254, primary_key=True) #primary key: authenticator
    user_id = models.CharField(max_length=200)#user_id_id
    date_created = models.DateTimeField('date created')#date created
    def __str__(self):
        return self.user_id.name