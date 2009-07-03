from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext,Context, loader
from django.core.urlresolvers import reverse
from django.test.client import Client

import os

from flash.models import Flash, FlashArchive

def create_user():
    user =  User.objects.create_user("user", "user@mail.com", "secret")
    return user

def create_flash():
    flash = Flash(title='flash_title')
    flash.save()
    return flash


class FlashTests(TestCase):
    
    def setUp(self):
        self.flash = create_flash()
    

class FlashUrlTests(TestCase):
    """
    These tests exercise the views.
    """
    def setUp(self):
        self.flash = create_flash()
        self.user = create_user()
        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()
       
    def test_flash_list(self):
        self.response = self.client.get(reverse("flash_flash_list"))
        self.assertEqual(self.response.status_code, 200)



