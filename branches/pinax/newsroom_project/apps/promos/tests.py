from django.core.urlresolvers import reverse
from django.test import TestCase

class PromoImageUrlTests(TestCase):
    def test_add_promo_image_get_url(self):
        self.response = self.client.get(reverse(
            "promos_promo_image_add",
            kwargs={}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_promo_link_get_url(self):
        self.response = self.client.get(reverse(
            "promos_promo_link_add",
            kwargs={}))
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