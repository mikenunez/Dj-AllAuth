from django.utils import timezone
from .models import Profile

import pytz

try:
	from django.utils.deprecation import MiddlewareMixin
except ImportError:  # Django < 1.10
	MiddlewareMixin = object

class TimezoneMiddleware(MiddlewareMixin):

	def process_request(self, request):
		if request.user.is_authenticated():
			pf = Profile.objects.filter(user=request.user.pk).first()
			tz = pf.timezone
			if tz:
				timezone.activate(pytz.timezone(tz))
			else:
				pass
		else:
			timezone.deactivate()
			