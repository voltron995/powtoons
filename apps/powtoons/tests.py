import json
from django.utils import timezone
from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.powtoons.models import Powtoon


class PowtoonAPITest(TestCase):

    def setUp(self):
        self.c = APIClient()

        self.admin_group = Group.objects.create(name='admin')
        ct = ContentType.objects.get_for_model(Powtoon)
        self.can_get_all_powtoons = Permission.objects.create(codename='can_get_all_powtoons',
                                                         name='Can get all powtoons',
                                                         content_type=ct
                                                         )

        self.can_share_powtoons = Permission.objects.create(codename='can_share_powtoons',
                                                       name='Can share powtoons',
                                                       content_type=ct
                                                       )

        self.admin_group.permissions.add(self.can_get_all_powtoons)
        self.admin_group.permissions.add(self.can_share_powtoons)

        self.admin = User.objects.create_user(
                username='admin_user',
                password='111',
                email='admin@gmail.com'
                )


        self.admin_group.user_set.add(self.admin)

        self.default_user = User.objects.create_user(
            username='default_user',
            password='111',
            email='default_user@gmail.com'
        )

        self.user_with_permission1 = User.objects.create_user(
            username='user_with_permission1',
            password='111',
            email='user_with_permission1@gmail.com'
        )
        self.user_with_permission1.user_permissions.add(self.can_get_all_powtoons)

        self.user_with_permission2 = User.objects.create_user(
            username='user_with_permission2',
            password='111',
            email='user_with_permission2@gmail.com'
        )
        self.user_with_permission2.user_permissions.add(self.can_share_powtoons)

        self.user_with_no_powtoons = User.objects.create_user(
            username='user_with_no_powtoons',
            password='111',
            email='user_with_no_powtoons@gmail.com'
        )
        self.powtoon1 = Powtoon.objects.create(
            name="First powtoon",
            owner=self.default_user,
            content={}
            )

        self.powtoon2 = Powtoon.objects.create(
            name="Second powtoon",
            owner=self.user_with_permission1,
            content={}
            )
        self.powtoon2.shared_with.add(self.default_user)

        self.powtoon3 = Powtoon.objects.create(
            name="Third powtoon",
            owner=self.user_with_permission2,
            content={}
            )



    def test_powtoons_list_for_default_user(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.get('/powtoon/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_powtoons_list_for_admin(self):
        self.c.login(username=self.admin.username, password='111')
        response = self.c.get('/powtoon/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_powtoons_list_for_user_with_no_powtoons(self):
        self.c.login(username=self.user_with_no_powtoons.username, password='111')
        response = self.c.get('/powtoon/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_powtoon_create(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.post('/powtoon/',
            data={
                    'name': 'New powtoon',
                    'owner': self.default_user.id,
                    'shared_with': [],
                },
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'name': "New powtoon",
            'owner': 2,
            'shared_with': []
        })

    def test_powtoon_details(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.get('/powtoon/{id}/'.format(id=self.powtoon1.id))
        self.assertEqual(response.data, {
            'id': response.data['id'],
            'name': "First powtoon",
            'owner': {
                'id': self.default_user.id,
                'username': "default_user"
            },
            'shared_with': []
        })

    def test_powtoon_edit(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.put('/powtoon/{id}/'.format(id=self.powtoon1.id),
            data={
                    'name': 'Renamed powtoon',
                },
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Renamed powtoon')

    def test_powtoon_delete(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.delete('/powtoon/{id}/'.format(id=self.powtoon1.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_powtoon_share(self):
        self.c.login(username=self.admin.username, password='111')
        response = self.c.patch('/powtoon/{id}/'.format(id=self.powtoon2.id),
            data={
                    'shared_with': [self.default_user.id]
                },
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['shared_with'], [self.default_user.id])

    def test_powtoon_share_no_permission(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.patch('/powtoon/{id}/'.format(id=self.powtoon2.id),
            data={
                    'shared_with': [self.admin.id]
                },
            format='json',
            )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            'detail': "You do not have permission to perform this action."
        })

    def test_powtoon_edit_no_permission(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.put('/powtoon/{id}/'.format(id=self.powtoon2.id),
            data={
                    'name': 'Renamed powtoon',
                },
            format='json',
            )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            'detail': "You do not have permission to perform this action."
        })

    def test_powtoon_details_no_permission(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.get('/powtoon/{id}/'.format(id=self.powtoon3.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            'detail': "You do not have permission to perform this action."
        })

    def test_powtoon_delete_no_permission(self):
        self.c.login(username=self.default_user.username, password='111')
        response = self.c.delete('/powtoon/{id}/'.format(id=self.powtoon2.id))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, {
            'detail': "You do not have permission to perform this action."
        })
