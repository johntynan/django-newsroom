from photos.models import Photo
import os.path
import os
from django.core.urlresolvers import reverse
from django.test import TestCase
from stories.tests import create_draft_story, create_user



class PhotoUrlTests(TestCase):
    """
    These tests exercise the views.
    """
    def setUp(self):
        self.user = create_user("user")
        self.story_draft = create_draft_story(
                headline="draft story",
                user=self.user)

        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()

    def test_add_photo_get_url(self):
        self.response = self.client.get(
            reverse("stories_story_add_media",
            kwargs={"story_id" : self.story_draft.id,
                "media_type" : "photo"}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_photo_post_url(self):
        try:
            TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
            photo = open(os.path.join(TESTS_DIR, "test_image.jpg"))
            self.response = self.client.post(
                reverse("stories_story_add_media",
                kwargs={"story_id" : self.story_draft.id,
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
        self.assertEqual(self.story_draft.get_relatedcontent(),
            {'photo': [Photo.objects.all()[0]]})
