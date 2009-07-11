from django.contrib.auth.models import User
from geotags.models import Point
from django.contrib.gis.utils.srs import add_postgis_srs
from django.core.urlresolvers import reverse
from django.test import TestCase
import os
from promos.models import Promo
from promos.models import PromoImage
from promos.models import PromoLink
from promos.models import PromoBillboard

def create_user(username):
    user =  User.objects.create_user(username, username+"@mail.com", "secret")
    return user

def create_promo(user):
    promo = Promo(headline='promo headline',
                    permalink='http://test.com',
                    relevance_begins='2009-02-03',
                    relevance_ends='2009-02-03')
    promo.submitter = user
    promo.save()
    promo.authors.add(user)
    promo.save()
    return promo


class PromoImageUrlTests(TestCase):
    def setUp(self):
        self.user = create_user("user")
        self.promo = create_promo(user=self.user)
        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()


    def test_add_promo_image_get_url(self):
        response = self.client.get(reverse(
            "promos_promo_image_add",
            kwargs={'promo_id':self.promo.id}))
        self.assertEqual(response.status_code, 200)

    def test_add_promo_image_post_url(self):
        try:
            TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
            image = open(os.path.join(TESTS_DIR, "test_image.jpg"))
            self.assertEqual(0, PromoImage.objects.count())
            response = self.client.post(reverse(
                "promos_promo_image_add",
                kwargs={'promo_id':self.promo.id}),
                {'attribution':'Mr Know',
                'caption':'excellent picture',
                'image_kind':'B',
                'image':image,
                })
            self.assertEqual(response.status_code, 302)
            self.assertEqual(1, PromoImage.objects.count())
        finally:
            image.close()

    def test_add_promo_link_get_url(self):
        response = self.client.get(reverse(
            "promos_promo_link_add",
            kwargs={'promo_id':self.promo.id}))
        self.assertEqual(response.status_code, 200)

    def test_add_promo_link_post_url(self):
        self.assertEqual(0, PromoLink.objects.count())
        response = self.client.post(reverse(
            "promos_promo_link_add",
            kwargs={'promo_id':self.promo.id}),
            {'title':'title link',
            'url': 'http://title.link.com'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, PromoLink.objects.count())

    def test_add_promo_list_get_url(self):
        response = self.client.get(reverse(
            "promos_promo_list",
            kwargs={}))
        self.assertEqual(response.status_code, 200)

    def test_add_promo_get_url(self):
        response = self.client.get(reverse(
            "promos_promo_add",
            kwargs={}))
        self.assertEqual(response.status_code, 200)

    def test_add_promo_post_url(self):
        self.assertEqual(1, Promo.objects.count())
        response = self.client.post(reverse(
            "promos_promo_add",
            kwargs={}),
            {'headline':'Add: promo headline',
            'permalink':'http://promos.csmonitor.com/promo_test/',
            'description':'description of the promo',
            'authors': (self.user.id,),
            'relevance_begins':'02/01/2009',
            'relevance_ends':'02/01/2009'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(2, Promo.objects.count())
        created_promo = Promo.objects.get(headline="Add: promo headline")
        self.assertEqual(response.context["user"],
                created_promo.authors.all()[0])

    def test_edit_promo_get_url(self):
        response = self.client.get(reverse(
            "promos_promo_edit",
            kwargs={"promo_id":self.promo.id}))
        self.assertEqual(response.status_code, 200)

    def test_edit_promo_post_url(self):
        self.assertEqual(1, Promo.objects.count())
        response = self.client.post(reverse(
            "promos_promo_edit",
            kwargs={"promo_id":self.promo.id}),
            {'headline':'promo headline modified',
            'permalink':'http://promos.csmonitor.com/promo_test/',
            'description':'description of the promo',
            'relevance_begins':'02/01/2009',
            'relevance_ends':'02/01/2009'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, Promo.objects.count())

    def test_add_point_post_url(self):
        add_postgis_srs(900913)
        self.assertEqual(0, Point.objects.count())
        response = self.client.post(reverse('promos_promo_add_edit_point',
            kwargs={"promo_id" : self.promo.id}),
            {"point" : "SRID=900913;POINT(-13161849.549963182 4036247.7234083386)"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, Point.objects.count())
        self.assertEqual(self.promo, Point.objects.all()[0].object)
        
    def test_add_billboard_url_post(self):
        # TODO : Improve this
        self.test_add_promo_image_post_url()
        
        self.assertEqual(1, Promo.objects.count())
        self.assertEqual(0, PromoBillboard.objects.count())
        response = self.client.post(reverse(
            "promos_promo_billboard_add",
            kwargs={"promo_id":self.promo.id}),
            {'headline':'Add: promo headline',
            'permalink':'http://promos.csmonitor.com/promo_test/',
            'description':'description of the promo',
            'headline_position_horizontal':100,
            'headline_position_vertical':100,
            'headline_width':300,
            'supporting_color':'#9ACD32',
            'headline_alignment':'left',
            'supporting_text_position_horizontal':0,
            'title':'tilte',
            'billboard_type':1,
            'supporting_text_width':100,
            'supporting_text_alignment':"left",
            'supporting_text_position_vertical':0,
            'supporting_text_color':'#9ACD32',
            'headline_color':'#9ACD32',
            'image':1
            })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(1, PromoBillboard.objects.count())
        
    def test_add_billboard_url_get(self):
        
        self.assertEqual(1, Promo.objects.count())
        response = self.client.get(reverse(
            "promos_promo_billboard_add",
            kwargs={"promo_id":self.promo.id}),
            {
            })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template[0].name,
                         'promos/promo_billboard_add_no_image.html')
        
        
