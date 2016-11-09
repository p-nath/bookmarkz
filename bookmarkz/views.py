from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from forms import *
#from django.template import RequestContext
from django.shortcuts import render
from bookmarkz_app.models import *
#from django.contrib.auth.decorators import login_required

def logout_page(request):
  logout(request)
  return HttpResponseRedirect('/')

def register(request):
  if request.method == 'POST':
    form = RegistrationForm(request.POST)
    if form.is_valid():
      user = User.objects.create_user(
        username=form.cleaned_data['username'],
        password=form.cleaned_data['password'],
        email=form.cleaned_data['email']
      )
      return HttpResponseRedirect('/')
  else:
    form = RegistrationForm()
  return render(
    request,
    '../templates/registration/register.html',
    {'form' : form,}
  )

def _bookmark_save(request, form):
  # Create or get link. (link = actual link, dummy = bool flag)
  link, dummy = Link.objects.get_or_create(
    url=form.cleaned_data['url']
  )
  # Create or get bookmark.
  bookmark, created = Bookmark.objects.get_or_create(
    user=request.user,
    link=link
  )
  # Update bookmark title.
  bookmark.title = form.cleaned_data['title']
  # If the bookmark is being updated, clear old tag list.
  if not created:
    bookmark.tag_set.clear()
  # Create new tag list.
  tag_names = form.cleaned_data['tags'].split()
  for tag_name in tag_names:
    tag, dummy = Tag.objects.get_or_create(name=tag_name)
    bookmark.tag_set.add(tag)
  # Save bookmark to database and return it.
  bookmark.save()
  return bookmark

@csrf_exempt
def bookmark_save_page(request):
  ajax = request.GET.has_key('ajax')
  if request.method == 'POST':
    form = BookmarkSaveForm(request.POST)
    if form.is_valid():
      bookmark = _bookmark_save(request, form)
      if ajax:
        return render(
          request,
          '../templates/bookmark_list.html',
        {
          'bookmarks': [bookmark],
          'show_edit': True,
          'show_tags': True
        })
      else:
        return HttpResponseRedirect(
          '/user/%s/' % request.user.username
        )
    else:
      if ajax:
        return HttpResponse('failure')
  elif request.GET.has_key('url'):
    url = request.GET['url']
    title = ''
    tags = ''
    try:
      link = Link.objects.get(url=url)
      bookmark = Bookmark.objects.get(link=link, user=request.user)
      title = bookmark.title
      tags = ' '.join(tag.name for tag in bookmark.tag_set.all())
    except:
      pass
    form = BookmarkSaveForm({
      'url': url,
      'title': title,
      'tags': tags
    })
  else:
    form = BookmarkSaveForm()
  if ajax:
    return render(
      request,
      '../templates/bookmark_save_form.html',
      {'form' : form,}
    )
  else:
    return render(
      request,
      '../templates/bookmark_save.html',
      {'form' : form,}
    )