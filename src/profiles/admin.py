from django.contrib import admin

from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _

from .models import Profile
from allauth.account.models import EmailAddress

# Register your models here

admin.site.unregister(User)
@admin.register(User)
class UserAdmin(BaseUserAdmin):
	fieldsets = (
		(None, {'fields': ('username', 'password', 'email_primary')}),
		(_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
									   'groups', 'user_permissions')}),
		(_('Important dates'), {'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2'),
		}),
	)
	list_display = ('username', 'email_primary', 'firstname', 'lastname', 'is_staff', 'is_active')
	list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
	search_fields = ('username', 'firstname', 'lastname', 'email_primary')
	ordering = ('username', )
	filter_horizontal = ('groups', 'user_permissions',)
	readonly_fields = ('firstname', 'lastname', 'email_primary',)


	def firstname(self, obj):
		p = Profile.objects.filter(user=obj).first()
		return p.firstname
	firstname.short_description = 'First Name'

	def lastname(self, obj):
		p = Profile.objects.filter(user=obj).first()
		return p.lastname
	lastname.short_description = 'Last Name'

	def email_primary(self, obj):
		e = EmailAddress.objects.filter(user=obj, primary=True).first()
		if e:
			if e.verified:
				return e.email
			else:
				e = _("Not Verified Yet")
				return e
		else:
			e = _("Not Primary Email")
			return e
	email_primary.short_description = 'Email Address'



@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	fieldsets = (
		(None, {'fields': ('user', 'email_primary',)}),
		(_('Personal Information:'), {'fields': ('firstname', 'lastname', 'avatar',
									   'phone', 'address', 'city', 'country')}),
		(_('Social Information:'), {'fields': ('facebook', 'twitter', 'instagram', 'linkedin')}),
	)

	list_display = ('user', 'email_primary', 'firstname', 'lastname', 'is_active',)
	ordering = ('user', 'firstname', 'lastname',)
	search_fields = ('user', 'firstname', 'lastname', 'email_primary',)
	readonly_fields = ('email_primary', 'is_active',)


	def email_primary(self, obj):
		e = EmailAddress.objects.filter(user=obj.user, primary=True).first()
		if e:
			if e.verified:
				return e.email
			else:
				e = _("Not Verified Yet")
				return e
		else:
			e = _("Not Primary Email")
			return e
	email_primary.short_description = 'Email Address'

	def is_active(self, obj):
		u = User.objects.filter(pk=obj.user.pk).first()
		return u.is_active
	is_active.boolean = True