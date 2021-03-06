from django.test import TestCase
from django.contrib.auth.models import User
from wiki.models import Page


class WikiTests(TestCase):
    def test_detail_page(self):
        # Instance of user to test the pages
        user = User.objects.create()

        # Create a test detail page
        Page.objects.create(title="Test", content="test content", author=user)

        # Making a GET request to the home page
        res = self.client.get('/')

        # Very a 200 response
        self.assertEqual(res.status_code, 200)
        result = res.context['pages']

        # Check if we got out test page
        self.assertQuerysetEqual(
            result,
            ['<Page: Test>']
        )

    def test_create_page(self):
        # Instance of user to test the pages
        user = User.objects.create()

        # Post data to be sent via the form
        post_data = {
            'title': 'Test',
            'content': 'test content',
            'author': user.id
        }

        # Request to create a post
        res = self.client.post('/create/', data=post_data)

        # Verify our response
        self.assertEqual(res.status_code, 302)

        # Get object to test
        page_object = Page.objects.get(title='Test')

        # Check that the page object was created in the test db
        self.assertEqual(page_object.title, 'Test')
