from django.test import TestCase
from ..models import Post


class PostTestCase(TestCase):
    def test_post(self):
        self.assertEquals(Post.objects.count(), 0)
        Post.objects.create(title='Post_1', content='Hi, this is my first post',  status=1)
        Post.objects.create(title='Post_2', content='Hi, this is my second post',  status=1)
        Post.objects.create(title='Post_3', content='Hi, this is my third post', status=0)
        Post.objects.create(title='Post_4', content='Hi, this is my fourht post', status=0)
        self.assertEquals(Post.objects.count(), 4)
        published_posts = Post.objects.filter(status=1)
        self.assertEquals(published_posts.count(), 2)
        drufted_posts = Post.objects.filter(status=0)
        self.assertEquals(drufted_posts.count(), 2)