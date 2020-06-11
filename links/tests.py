from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from links.models import Link
from links.views import get_tiny_link, open_tiny_link


def create_tiny_link(orig_link):
    link = Link.objects.create(
        orig_link=orig_link,
        tiny_link=get_tiny_link(orig_link=orig_link)
    )
    link.save()
    return link


class LinkModelTests(TestCase):

    def test_get_tiny_link(self):
        """
            get_tiny_link() returns tiny link for original link
        """
        tiny_link = get_tiny_link("https://google.com/")
        self.assertIsNotNone(tiny_link)

    def test_increase_follow_quantity(self):
        """
            follow_quantity field of new link after increase returns 1
        """
        link = create_tiny_link("https://google.com/")
        link.follow_quantity += 1
        link.save()
        self.assertIs(link.follow_quantity, 1)


class LinkIndexViewTests(TestCase):

    def test_created_link(self):
        """
            response contains tiny link of just created link
        """
        link = create_tiny_link("https://google.com/")
        url = reverse('links:index')
        response = self.client.get(url)
        self.assertContains(response, link.tiny_link)

    def test_deleted_link(self):
        """
            response not contains link of just deleted link
        """
        link = create_tiny_link("https://google.com/")
        link.delete()
        url = reverse('links:index')
        response = self.client.get(url)
        self.assertNotContains(response, link.orig_link)

    def test_nonexistent_link(self):
        """
            response not contains link of nonexistent link
        """
        url = reverse('links:index')
        response = self.client.get(url)
        orig_link = "https://byrbalyalya/"
        self.assertNotContains(response, orig_link)

    def test_open_link(self):
        """
            response redirects to the original link after open tiny link
        """
        link = create_tiny_link("https://vk.com/")
        url = reverse('links:open', args=(link.tiny_link,))
        response = self.client.get(url)
        self.assertRedirects(response,
                             link.orig_link,
                             status_code=302,
                             target_status_code=200,
                             msg_prefix='',
                             fetch_redirect_response=False)

    def test_increase_follow_quantity_after_open_link(self):
        """
            follow_quantity field of created link after its open increases by one
        """
        link = create_tiny_link("https://vk.fun/")
        url = reverse('links:open', args=(link.tiny_link,))
        self.client.get(url)
        updated_link = get_object_or_404(Link, tiny_link=link.tiny_link)
        self.assertIs(updated_link.follow_quantity, link.follow_quantity + 1)
