from __future__ import unicode_literals
from django.contrib import messages
from django.db import models
import bcrypt
import re

EMAIL_REGEX = re.compile (r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
  def isValidRegistration(self, userInfo):
    passFlag = True
    errors = []
    success = []
    if len(userInfo['first_name']) < 2:
      errors.append('First name must be at least 2 characters.')
      passFlag = False
    if len(userInfo['first_name']) > 0:
      if not userInfo['first_name'].isalpha():
        errors.append('First name contains non-alpha character(s)')
        passFlag = False
    if len(userInfo['last_name']) < 2:
      errors.append('Last name must be at least 2 characters.')
      passFlag = False
    if len(userInfo['last_name']) > 0:
      if not userInfo['last_name'].isalpha():
        errors.append('Last name contains non-alpha character(s)')
        passFlag = False
    if not EMAIL_REGEX.match(userInfo['email']):
      errors.append('Email provided is invalid.')
      passFlag = False
    if len(userInfo['password']) < 8:
      errors.append('Password must contain at least 8 characters.')
      passFlag = False
    if userInfo['password'] != userInfo['confirm_password']:
      errors.append('Passwords do not match.')
      passFlag = False
    if len(self.filter(email=userInfo['email'])) > 0:
      errors.append("Registration is invalid.")
      passFlag = False

    if passFlag == True:
      success.append("You have successfully registered. Please log in.")
      hashed = bcrypt.hashpw(userInfo['password'].encode(), bcrypt.gensalt())
      self.create(first_name = userInfo['first_name'], last_name = userInfo['last_name'], email = userInfo['email'], password = hashed, city = userInfo['city'], state = userInfo['state'])
      return [passFlag, errors, success]

  def ValidLogin(self, userInfo):
    passFlag = True
    errors = []
    if len(self.filter(email=userInfo['email'])) > 0:
      hashed = User.objects.get(email = userInfo['email']).password
      hashed = hashed.encode('utf-8')
      password = userInfo['password']
      password = password.encode('utf-8')
      if bcrypt.hashpw(password, hashed) == hashed:
        passFlag = True
      else:
        errors.append("Unsuccessful login.")
        passFlag = False
    else:
      errors.append("Unsuccessful login.")
      passFlag = False
    return [passFlag, errors]

class User(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  email = models.EmailField()
  password = models.CharField(max_length=250)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=25)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()
  userManager = UserManager()

class GroupManager(models.Manager):
  def isValidGroup(self, userInfo, userFiles):
    passFlag = True
    errors = []
    if len(userInfo['group_name']) < 3:
      errors.append('Group name must be at least 3 characters.')
      passFlag = False
    if len(userInfo['description']) < 10:
      errors.append('Group description must be 10 characters or more.')
      passFlag = False

    if passFlag == True:
      self.create(group_name = userInfo['group_name'], description=userInfo['description'], photo=userFiles['photo'])
    return [passFlag, errors]

class Group(models.Model):
  group_name = models.CharField(max_length=50)
  description = models.CharField(max_length=250)
  photo = models.ImageField(upload_to='group_photos', default='images/default_group.jpg')
  grouped_users_id = models.ManyToManyField(User, related_name="grouped_users")
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = models.Manager()
  groupManager = GroupManager()

class Recipe(models.Model):
  name = models.CharField(max_length=255)
  user = models.ForeignKey(User)
  product_pic = models.ImageField(upload_to='recipes', default=None)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Ingredient(models.Model):
  name = models.CharField(max_length=255)
  quantity = models.CharField(max_length=255)
  recipe = models.ForeignKey(Recipe)

class Step(models.Model):
  step_number = models.IntegerField(default=0)
  direction = models.TextField()
  recipe = models.ForeignKey(Recipe)