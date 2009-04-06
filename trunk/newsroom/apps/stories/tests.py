from django.test import TestCase
from django.template.defaultfilters import slugify
from stories.models import Story, StoryIntegrityError

class StoryTests(TestCase):
    
    def setUp(self):
        self.story = self.create_story()
    
    def create_story(self):
        story = Story()
        story.headline = "This Is A Test Story"
        #normally slugify will be handled by the UI 
        story.slug = slugify(story.headline)
        summary = "Like I said in the headline, this is a test story."
        #TODO add an author
        story.save()
        return story
    
    def test_create_story(self):
        self.failUnlessEqual(self.story.pages.count(),1,"New stories should have exactly one page")
        self.failUnlessEqual(self.story.pages[0].pagenum,1,"First page should be 1")
        
    def test_story_always_has_one_or_more_pages(self):
        p1 = self.story.pages[0]
        self.assertRaises(StoryIntegrityError,p1.delete)
        
    def test_story_add_page(self):
        new_page = self.story.add_page()
        self.failUnlessEqual(new_page.pagenum,2,"This should be the second page for the story")
        self.failUnlessEqual(self.story.pages.count(),2,"This should be the second page for the story")
        