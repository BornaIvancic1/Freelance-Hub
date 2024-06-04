from django.test import TestCase, Client
from django.urls import reverse
from Projekt.models import Korisnik, Tvrtka, Freelancer,Posao,ObjavaPosla
from django.contrib.auth.models import Group

class MeViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ja_view(self):
       
        user = Korisnik.objects.create_user(
            email='testuser@example.com',
            password='password'
        )

       
        tvrtka = Tvrtka.objects.create(user=user)
        freelancer = Freelancer.objects.create(user=user)


        self.client.login(email='testuser@example.com', password='password')

      
        response = self.client.get(reverse('ja'))  

    
      
        self.assertEqual(response.status_code, 302)
     
        self.client.logout()

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_login_view(self):
       
        user = Korisnik.objects.create_user(
            email='testuser@example.com',
            password='password'
        )

        tvrtka = Tvrtka.objects.create(user=user)
        freelancer = Freelancer.objects.create(user=user)

    
        response = self.client.post(reverse('login')) 

       
        self.assertEqual(response.status_code, 302)

     
        login_data = {'email': 'testuser@example.com', 'password': 'password'}
        response = self.client.post(reverse('login'), data=login_data)

       
        self.assertEqual(response.status_code, 302)

      
        self.assertTrue(Korisnik.objects.get(email='testuser@example.com').is_authenticated)



class PocetnaViewTests(TestCase):
    def setUp(self):
        self.client = Client()

        posao = Posao.objects.create(naziv_posla='Software Developer')
        objava_posla = ObjavaPosla.objects.create(
            naslov='Posao1',
            sadrzaj='Opis posla',
            datum_objave='2024-01-22',
            datum_isteka='2024-02-22',
            posao=posao
        )

        Group.objects.create(name='Freelancer')
        Group.objects.create(name='Tvrtka')

        self.freelancer_user = Korisnik.objects.create_user(
            email='freelancer@example.com',
            password='password',
            first_name='FreelancerFirstName',
            last_name='FreelancerLastName',
            username='freelancer_username'
        )
        self.freelancer_user.groups.add(Group.objects.get(name='Freelancer'))

    def test_pocetna_view_rendering(self):
        response = self.client.get(reverse('pocetna'))  

        if response.status_code == 302:
            response = self.client.get(response.url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Objave poslova")
        self.assertContains(response, "Modal Header Content")