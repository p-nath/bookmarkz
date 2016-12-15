from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404

from bookmarkz_app.models import Bookmark
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

class RecentBookmarks(Feed):
	title = 'Django Bookmarks | Recent Bookmarks'
	link = '/feed/recent/'
	description = 'Recent bookmarks posted to Django Bookmarks'

	def items(self):
		return Bookmark.objects.order_by('-id')[:10]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		pass

class UserBookmarks(Feed):

	def get_object(self, request, username):
		return get_object_or_404(User, username=username)

	def title(self, user):
		return 'Django Bookmarks | Bookmarks for %s' % user.username

	def link(self, user):
		return '/feeds/user/%s/' % user.username

	def description(self, user):
		return 'Recent bookmarks posted by %s' % user.username

	def items(self, user):
		return user.bookmark_set.order_by('-id')[:10]

	def item_title(self, item):
		return item.title

	def item_description(self, item):
		pass

