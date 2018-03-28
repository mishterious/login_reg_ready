from __future__ import unicode_literals
import re, datetime, time
from django.db import models

ALL_LETTERS_REGEX = re.compile(r'[A-Za-z]+')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def basic_validator(self, postData):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        errors = {}
        email = postData['email'].lower()
        if len(postData['name']) < 3:
            errors['name'] = "Your name should be at least 3 letters long and should only be letters"
        if len(email) < 1:
            errors['email'] = "Please enter an e-mail address"
        if not EMAIL_REGEX.match(email):
            errors['email2'] = "Please enter a Valid e-mail address"
        if re.search('[0-9]', postData['password']) is None:
            errors['numpass'] = "You need to enter at least one number to make your password Valid"
        if re.search('[A-Z]', postData['password']) is None:
            errors['capspass'] = "You will need to enter at least one capital letter"
        if len(postData['password']) < 8:
            errors['lenpass'] = "Your password needs to be at least 8 character to be Valid"
        elif postData['password'] != postData['password_confirm']:
            errors['mispass'] = "Your passwords do not match"
        user = User.objects.filter(email=email)
        if len(user) > 0:
            errors['user'] = "User already exists in the database"

        return errors


class QuoteManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['insp']) == 0: 
            errors['insp_blank'] = "It seems like there should be more."
        if len(postData['quote_by']) == 0: 
            errors['who_blank'] = "Who made this quote???"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Quote(models.Model):
    insp = models.CharField(max_length=255)
    quote_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='my_contribution')
    users = models.ManyToManyField(User, related_name="liked")
    objects = QuoteManager()

    def __repr__(self):
        return "<Blog object: {} {} {} {}>".format(self.insp, self.quote_by, self.user, self.users)