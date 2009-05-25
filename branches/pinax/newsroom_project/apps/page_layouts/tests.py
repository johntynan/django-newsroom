from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext,Context, loader
from django.core.urlresolvers import reverse
from django.test.client import Client
from page_layouts.models import PageLayout
from page_layouts.views import page_layout_list

def create_user():
    user =  User.objects.create_user("user", "user@mail.com", "secret")
    return user


def create_page_layout():
    page_layout = PageLayout()
    page_layout.title = "This Is A Test Page Layout"
    page_layout.html = "<p>html here</p>"
    page_layout.description = "Like I said, this is a test page layout."
    page_layout.image = "images/widgets/page_layouts/one_column.png"
    page_layout.save()

    c = Client()
    response = c.get('/page_layouts/index.json')
    response.status_code



class PageLayoutTests(TestCase):
    
    def setUp(self):
        self.page_layout = create_page_layout()
    

class PageLayoutUrlTests(TestCase):
    """
    These tests exercise the views.
    """
    def setUp(self):
        self.page_layout = create_page_layout()
        self.user = create_user()
        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()
       
    def test_page_layout_list(self):
        self.response = self.client.get(reverse("page_layout_list"))
        self.assertEqual(self.response.status_code, 200)

