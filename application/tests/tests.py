import json
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from django.urls import reverse
from ..models import Post
from ..serializers import PostSerializer
from users.models import User


class RegisterUserTest(TestCase):
    def test_register(self):
        url = reverse('register_user')
        response = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthoriseTest(TestCase):
    def test_authorize(self):
        url = reverse('authenticate_user')
        u = User.objects.create(email='vromanko@ucu.edu.ua', first_name='Veronika', last_name='Romanko',
                                password='password')
        u.save()
        response = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LikeUnlikeTest(TestCase):
    def setUp(self):
        self.post_1 = Post.objects.create(title='Post_1', content='Hi, this is my first post', status=1)
        self.test_data = {}

        url = reverse('register_user')
        self.user = self.client.post(url,
                                     {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                      'password': 'password'}, format='json')
        url = reverse('authenticate_user')
        response = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        self.token = str(response.data['token']).split("'")[1] + str(response.data['token']).split("'")[2]

    def test_like_unlike_post(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())
        # get API response
        response = self.client.put(
            reverse('like_post', kwargs={'pk': self.post_1.pk}),
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['like'], True)

        response = self.client.put(
            reverse('unlike_post', kwargs={'pk': self.post_1.pk}),
            data=json.dumps(self.test_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['like'], False)


class GetAllPostsTest(TestCase):
    def setUp(self):
        Post.objects.create(title='Post_1', content='Hi, this is my first post', status=1)
        Post.objects.create(title='Post_2', content='Hi, this is my second post', status=1)
        Post.objects.create(title='Post_3', content='Hi, this is my third post', status=0)
        Post.objects.create(title='Post_4', content='Hi, this is my fourht post', status=0)

        url = reverse('register_user')
        self.user = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        url = reverse('authenticate_user')
        response = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        self.token = str(response.data['token']).split("'")[1] + str(response.data['token']).split("'")[2]

    def test_get_all_posts(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())
        # get API response
        response = self.client.get(reverse('get_post_posts'))
        # get data from db
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSinglePostTest(TestCase):
    def setUp(self):
        self.post_1 = Post.objects.create(title='Post_1', content='Hi, this is my first post', status=1)
        self.post_2 = Post.objects.create(title='Post_2', content='Hi, this is my second post', status=1)
        self.post_3 = Post.objects.create(title='Post_3', content='Hi, this is my third post', status=0)
        self.post_4 = Post.objects.create(title='Post_4', content='Hi, this is my fourht post', status=0)

        url = reverse('register_user')
        self.user = self.client.post(url,
                                     {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                      'password': 'password'}, format='json')
        url = reverse('authenticate_user')
        response = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        self.token = str(response.data['token']).split("'")[1] + str(response.data['token']).split("'")[2]

    def test_get_valid_single_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())

        response = client.get(reverse('get_delete_update_post', kwargs={'pk': self.post_1.pk}))
        post = Post.objects.get(pk=self.post_1.pk)
        serializer = PostSerializer(post)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())

        response = client.get(reverse('get_delete_update_post', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewPostTest(TestCase):
    def setUp(self):
        self.valid_post = {
            'title': 'Post_1',
            'content': 'Hi, this is my first post',
            'status': 0
        }
        self.invalid_post = {
            'title': '',
            'content': 'Hi, this is my second post',
            'status': 1
        }

        url = reverse('register_user')
        self.user = self.client.post(url,
                                     {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                      'password': 'password'}, format='json')
        url = reverse('authenticate_user')
        response = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        self.token = str(response.data['token']).split("'")[1] + str(response.data['token']).split("'")[2]

    def test_create_valid_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())
        response = client.post(reverse('get_post_posts'),
            data=json.dumps(self.valid_post),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())
        response = client.post(
            reverse('get_post_posts'),
            data=json.dumps(self.invalid_post),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSinglePostTest(TestCase):
    def setUp(self):
        self.post_1 = Post.objects.create(title='Post_1', content='Hi, this is my first post', status=1)
        self.post_2 = Post.objects.create(title='Post_2', content='Hi, this is my second post', status=1)
        self.valid_post = {
            'title': 'Post_1',
            'content': 'Hi, this is my first post',
            'status': 0
        }
        self.invalid_post = {
            'title': '',
            'content': 'Hi, this is my second post',
            'status': 1
        }

        url = reverse('register_user')
        self.user = self.client.post(url,
                                     {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                      'password': 'password'}, format='json')
        url = reverse('authenticate_user')
        response = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        self.token = str(response.data['token']).split("'")[1] + str(response.data['token']).split("'")[2]

    def test_valid_update_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())
        response = client.put(
            reverse('get_delete_update_post', kwargs={'pk': self.post_1.pk}),
            data=json.dumps(self.valid_post),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_update_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())
        response = client.put(
            reverse('get_delete_update_post', kwargs={'pk': self.post_1.pk}),
            data=json.dumps(self.invalid_post),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteSinglePostTest(TestCase):
    def setUp(self):
        self.post_1 = Post.objects.create(title='Post_1', content='Hi, this is my first post', status=1)
        self.post_2 = Post.objects.create(title='Post_2', content='Hi, this is my second post', status=1)
        url = reverse('register_user')
        self.user = self.client.post(url,
                                     {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                      'password': 'password'}, format='json')
        url = reverse('authenticate_user')
        response = self.client.post(url,
                                    {'email': 'vromanko@ucu.edu.ua', 'first_name': 'Veronika', 'last_name': 'Romanko',
                                     'password': 'password'}, format='json')
        self.token = str(response.data['token']).split("'")[1] + str(response.data['token']).split("'")[2]

    def test_valid_delete_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())
        response = client.delete(
            reverse('get_delete_update_post', kwargs={'pk': self.post_1.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_post(self):
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(self.token).encode())
        response = client.delete(
            reverse('get_delete_update_post', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
