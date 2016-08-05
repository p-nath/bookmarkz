from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import *
from forms import *
from django.shortcuts import get_object_or_404

def main_page(request):
  return render_to_response(
    'main_page.html', RequestContext(request)
  )

def user_page(request, username):
  user = get_object_or_404(User, username=username)
  bookmarks = user.bookmark_set.order_by('-id')
  bookmarks = user.bookmark_set.all()
  variables = RequestContext(request, {
    'username': username,
    'bookmarks': bookmarks,
    'show_tags': True
  })
  return render_to_response('user_page.html', variables)
 
def tag_page(request, tag_name):
  tag = get_object_or_404(Tag, name=tag_name)
  bookmarks = tag.bookmarks.order_by('-id')
  variables = RequestContext(request, {
    'bookmarks': bookmarks,
    'tag_name': tag_name,
    'show_tags': True,
    'show_user': True
  })
  return render_to_response('tag_page.html', variables)

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
  variables = RequestContext(request, {
    'tags': tags
  })
  return render_to_response('tag_cloud_page.html', variables)

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
  variables = RequestContext(request, { 'form': form,
    'bookmarks': bookmarks,
    'show_results': show_results,
    'show_tags': True,
    'show_user': True
  })
  return render_to_response('search.html', variables)
