from videos.models import Video
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

class VideoUrlTests(TestCase):
    """
    These tests exercise the views.
    """
    def setUp(self):
        self.story = create_story()
        self.user = create_user()
        self.client.login(username="user", password="secret")
    def tearDown(self):
        self.client.logout()

    def test_add_video_get_url(self):
        self.response = self.client.get(
            reverse("stories_story_add_media",
            kwargs={"story_id" : self.story.id,
                "media_type" : "video"}))
        self.assertEqual(self.response.status_code, 200)

    def test_add_video_post_url(self):
        try:
            TESTS_DIR = os.path.abspath(os.path.dirname(__file__))
            frame = open(os.path.join(TESTS_DIR, "test_frame.jpg"))
            video =  open(os.path.join(TESTS_DIR, "test_video.flv"))
            self.response = self.client.post(
                reverse("stories_story_add_media",
                kwargs={"story_id" : self.story.id,
                    "media_type" : "video"}),
                    {
                        "title":"test picture",
                        "status":"D",
                        "license":"http://creativecommons.org/licenses/by/2.0/",
                         "authors" : (self.user.id,),
                         "sites" : (1,),
                         "video":video,
                         "frame":frame,
                    })
        finally:
            frame.close()
            video.close()
        self.assertEqual(self.response.status_code, 302)
        # Check if the photo as been created
        self.assertEqual(1, Video.objects.count())
