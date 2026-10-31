from django.test import TestCase
from django.urls import reverse

from .models import ContactInquiry


class ContactPageTests(TestCase):
    def test_contact_page_renders(self):
        response = self.client.get(reverse('main:contacts'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Send Us a Message')

    def test_contact_form_submission_persists_inquiry(self):
        response = self.client.post(
            reverse('main:contacts'),
            {
                'first_name': 'John',
                'last_name': 'Doe',
                'email': 'john@example.com',
                'phone': '+1234567890',
                'subject': 'Need legal help',
                'service': 'civil',
                'message': 'I need advice regarding a civil dispute.',
                'terms': 'on',
            },
            follow=True,
        )

        self.assertRedirects(response, reverse('main:contacts'))
        self.assertEqual(ContactInquiry.objects.count(), 1)
        self.assertContains(response, 'Thank you for your message.')
