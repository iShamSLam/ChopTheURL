import bcrypt as bcrypt
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Link

# out pages models
class IndexView(generic.ListView):
    template_name = 'links/index.html'
    context_object_name = 'links_list'

    def get_queryset(self):
        return Link.objects.filter().order_by('-follow_quantity')


class CreateView(generic.CreateView):
    template_name = 'links/new.html'
    model = Link
    fields = ['orig_link']


class DetailView(generic.DetailView):
    model = Link
    pk_url_kwarg = 'link_id'
    template_name = 'links/detail.html'


def get_tiny_link(orig_link):
    tiny_link = bcrypt.hashpw(orig_link.encode('utf-8'), bcrypt.gensalt())
    return tiny_link.decode("utf-8")[40:50].replace('/', '')


def create_tiny_link(request):
    orig_link = request.POST['orig_link']
    link = Link.objects.create(
        orig_link=orig_link,
        tiny_link=get_tiny_link(orig_link=orig_link)
    )
    link.save()
    return HttpResponseRedirect(reverse('links:detail', args=(link.id,)))


def open_tiny_link(request, tiny_link):
    link = get_object_or_404(Link, tiny_link=tiny_link)
    orig_link = link.orig_link
    link.follow_quantity += 1
    link.save()
    return HttpResponseRedirect(orig_link)


def delete_tiny_link(request, link_id):
    link = get_object_or_404(Link, id=link_id)
    link.delete()
    return HttpResponseRedirect(reverse('links:index'))
