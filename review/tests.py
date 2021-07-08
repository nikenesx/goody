from django.test import TestCase, Client
from review.models import Doctor, Review
from django.contrib.auth.models import User
import factory


class DocFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Doctor
    doctor_name = 'doctor'


class ReviewFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Review
    review_doctor = factory.SubFactory(DocFactory)
    original_rev_text = '!! ! СПАСИБО ЧТо ПоМоГЛиии....    У ра !! ,!!?????'
    processed_rev_text = ''
    ip_address = '127.0.0.1'


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    username = factory.Faker('user_name')
    password = 'secret123'
    is_staff = False


class ViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.doctor = DocFactory()

    def setUp(self):
        self.client = Client(HTTP_USER_AGENT='Mozilla/5.0')

    def test_view_review(self):
        user = UserFactory(is_staff=True)
        self.client.force_login(user)
        response = self.client.get('/review')
        self.assertEqual(response.status_code, 200)

        user2 = UserFactory()
        self.client.force_login(user2)
        response = self.client.get('/review')
        self.assertEqual(response.status_code, 404)

    def test_view_get(self):
        doctor = self.doctor
        response = self.client.get(f'/add-review/{doctor.id}/')

        self.assertEqual(response.status_code, 200)

    def test_view_post(self):
        review = 'this is a review'
        doctor = self.doctor
        response = self.client.post(f'/add-review/{doctor.id}/', {'review_text': review})
        obj_rev = doctor.review_set.first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(review, obj_rev.original_rev_text)


class ReviewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.review = ReviewFactory()

    def test_remake_rev(self):
        valid_review = '! ! Спасибо что помоглиии. У ра! , ! ?'
        self.assertEqual(valid_review, self.review.remake_rev())
