from django.test import TestCase, Client
from .models import FAQ
from django.core.cache import cache


class FAQModelTest(TestCase):
    def setUp(self):
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a Python web framework.",
            question_hi="Django क्या है?",
            question_bn="Django কি?",
        )

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, "What is Django?")
        self.assertEqual(self.faq.answer, "Django is a Python web framework.")

    def test_translation_method(self):
        self.assertEqual(
            self.faq.get_translated_question("hi"), "Django क्या है?"
        )
        self.assertEqual(self.faq.get_translated_question("bn"), "Django কি?")
        self.assertEqual(
            self.faq.get_translated_question("en"), "What is Django?"
        )


class FAQAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.faq = FAQ.objects.create(
            question="What is Django?",
            answer="Django is a Python web framework.",
            question_hi="Django क्या है?",
            question_bn="Django কি?",
        )

    def test_faq_api(self):
        response = self.client.get('/api/faqs/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "What is Django?")

    def test_faq_api_with_translation(self):
        response = self.client.get('/api/faqs/?lang=hi')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['question'], "Django क्या है?")

    def test_cache_invalidation(self):
        cache_key = f'faq_{self.faq.id}'
        self.faq.save()
        self.assertIsNone(cache.get(cache_key))
