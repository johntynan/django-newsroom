from django.core.urlresolvers import reverse
from django.test import TestCase
from promos.models import Promo
from django.contrib.auth.models import User

def create_user():
    user = User.objects.create_user(username="joe",
        password="secret",
        email="joe@foo.com")
    user.save()
    return user

def create_promo(user):
    promo = Promo(headline='promo headline',
                    permalink='http://test.com',
                    relevance_begins='2009-02-03',
                    relevance_ends='2009-02-03')
    promo.submitter = user
    promo.save()
    return promo

class PromoImageUrlTests(TestCase):
    def setUp(self):
        self.user = create_user()
        self.promo = create_promo(user=self.user)


    def test_add_promo_image_get_url(self):
        self.response = self.client.get(reverse(
            "promos_promo_image_add",
            kwargs={'promo_id':self.promo.id}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_promo_link_get_url(self):
        self.response = self.client.get(reverse(
            "promos_promo_link_add",
            kwargs={'promo_id':self.promo.id}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_promo_list_get_url(self):
        self.response = self.client.get(reverse(
            "promos_promo_list",
            kwargs={}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_promo_get_url(self):
        self.response = self.client.get(reverse(
            "promos_promo_add",
            kwargs={}))
        self.assertEqual(self.response.status_code, 200)