from photos.models import Photo
import os.path
import os
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.template.defaultfilters import slugify
from stories.models import Story

def create_story():
    story = Story()
    story.headline = "This Is A Test Story"
    #normally slugify will be handled by the UI
    story.slug = slugify(story.headline)
    story.summary = "Like I said in the headline, this is a test story."
    #TODO add an author(s)
    story.save()
    return story

def create_user():
    user =  User.objects.create_user("user", "user@mail.com", "secret")
    return user

class PhotoUrlTests(TestCase):
    """
    These tests exercise the views.
    """
    def setUp(self):
        self.story = create_story()
        self.user = create_user()
        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()

    def test_add_photo_get_url(self):
        self.response = self.client.get(
            reverse("stories_story_add_media",
            kwargs={"story_id" : self.story.id,
                "media_type" : "photo"}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_photo_post_url(self):
        try:
            TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
            photo = open(os.path.join(TESTS_DIR, "test_image.jpg"))
            self.response = self.client.post(
                reverse("stories_story_add_media",
                kwargs={"story_id" : self.story.id,
                    "media_type" : "photo"}),
                    {
                        "title":"test picture",
                        "status":"D",
                        "license":"http://creativecommons.org/licenses/by/2.0/",
                         "authors" : (self.user.id,),
                         "sites" : (1,),
                         "image":photo,
                    })
        finally:
            photo.close()
        
        self.assertEqual(self.response.status_code, 302)
        # Check if the photo as been created
        self.assertEqual(1, Photo.objects.count())
