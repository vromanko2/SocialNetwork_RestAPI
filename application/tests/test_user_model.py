from django.test import TestCase
from users.models import User


class UserTestCase(TestCase):
    def test_user(self):
        self.assertEquals(User.objects.count(), 0)
        User.objects.create(email='vromanko@ucu.edu.ua', first_name='Veronika',  last_name='Romanko', password='1')
        User.objects.create(email='vromanko2@ucu.edu.ua', first_name='Veronika',  last_name='Romanko_2', password='12')
        User.objects.create(email='vromanko3@ucu.edu.ua', first_name='Veronika_2',  last_name='Romanko_3', password='123')
        User.objects.create(email='vromanko4@ucu.edu.ua', first_name='Veronika_2',  last_name='Romanko_4', password='1234')
        self.assertEquals(User.objects.count(), 4)
        users_veronika = User.objects.filter(first_name='Veronika')
        self.assertEquals(users_veronika.count(), 2)
        users_veronika_2 = User.objects.filter(first_name='Veronika_2')
        self.assertEquals(users_veronika_2.count(), 2)
