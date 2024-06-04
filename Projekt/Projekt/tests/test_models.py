from django.test import TestCase
from django.contrib.auth import get_user_model
from Projekt.models import *


class TvrtkaModelTest(TestCase):
    def test_tvrtka_creation(self):
        user = get_user_model().objects.create(email='tvrtka@example.com', password='password')
        tvrtka = Tvrtka.objects.create(user=user)
        self.assertEqual(tvrtka.user, user)

class FreelancerModelTest(TestCase):
    def test_freelancer_creation(self):
        user = get_user_model().objects.create(email='freelancer@example.com', password='password')
        freelancer = Freelancer.objects.create(user=user)
        self.assertEqual(freelancer.user, user)

class PosaoModelTest(TestCase):
    def test_posao_creation(self):
        posao = Posao.objects.create(naziv_posla='Software Developer')
        self.assertEqual(posao.naziv_posla, 'Software Developer')

class ObjavaPoslaModelTest(TestCase):
    def test_objava_posla_creation(self):
        posao = Posao.objects.create(naziv_posla='Software Developer')
        objava_posla = ObjavaPosla.objects.create(
            naslov='Job Opening',
            sadrzaj='We are hiring!',
            datum_objave='2024-01-20',
            datum_isteka='2024-02-20',
            posao=posao
        )
        self.assertEqual(objava_posla.naslov, 'Job Opening')