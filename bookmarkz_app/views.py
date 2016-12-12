from django.http import HttpResponse
from django.shortcuts import render
'''from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.template import RequestContext'''
from models import *
from forms import *
from django.shortcuts import get_object_or_404

def main_page(request):
  shared_bookmarks = SharedBookmark.objects.order_by(
    '-date'
  )[:10]
  return render(
    request,
    '../templates/main_page.html',{
    'shared_bookmarks': shared_bookmarks
  })

def user_page(request, username):
  user = get_object_or_404(User, username=username)
  bookmarks = user.bookmark_set.order_by('-id')
  bookmarks = user.bookmark_set.all()
  return render(
    request,
    '../templates/user_page.html', {
    'username': username,
    'bookmarks': bookmarks,
    'show_tags': True,
    'show_edit': username == request.user.username,
  })
 
def tag_page(request, tag_name):
  tag = get_object_or_404(Tag, name=tag_name)
  bookmarks = tag.bookmarks.order_by('-id')
  return render(
    request,
    '../templates/tag_page.html', {
    'bookmarks': bookmarks,
    'tag_name': tag_name,
    'show_tags': True,
    'show_user': True
  })

def tag_cloud_page(request):
  MAX_WEIGHT = 5
  tags = Tag.objects.order_by('name')
  # calculating min and max
  min_count = max_count = tags[0].bookmarks.count()
  for tag in tags:
    tag.count = tag.bookmarks.count()
    if tag.count < min_count:
      min_count = tag.count
    if max_count < tag.count:
      max_count = tag.count
  # Calculate count range. Avoid dividing by zero.
  count_range = float(max_count - min_count)
  if count_range == 0.0:
    count_range = 1.0
  # Calculate tag weights.
  for tag in tags:
    tag.weight = int(
      MAX_WEIGHT * (tag.count - min_count) / count_range
    )
  return render(
    request,
    '../templates/tag_cloud_page.html', {
    'tags': tags
  })

def search_page(request):
  form = SearchForm()
  bookmarks = []
  show_results = False
  if request.GET.has_key('query'):
    show_results = True
    query = request.GET['query'].strip()
    if query:
      form = SearchForm({'query' : query})
      bookmarks = \
        Bookmark.objects.filter (title__icontains=query)[:10]
  if request.GET.has_key('ajax'):
    return render(
    request,
    '../templates/bookmark_list.html', {
    'form': form,
    'bookmarks': bookmarks,
    'show_results': show_results,
    'show_tags': True,
    'show_user': True
  })
  else:
    return render(
    request,
    '../templates/search.html',
    {
    'form': form,
    'bookmarks': bookmarks,
    'show_results': show_results,
    'show_tags': True,
    'show_user': True
  })
