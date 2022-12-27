from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here.
from user.models import ProfilePro, UserProfile, Releve


class UserProfileAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['user_name','mission','nom_societe','address','phone','city','country','created','updated','image_tag']
    list_filter = ('updated',)

class ProfileProAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ['user','raison_social','compte','ville','catalog','releve', 'status', 'created']
    list_filter = ('catalog','releve','ville', 'created','status')
    list_editable = ('catalog',"releve","status",)


class releveAdmin(ImportExportModelAdmin):
	list_display = ('id','compte','date_fac','ref_fac','mnt_ttc','mnt_regler','solde','created',)
	list_filter = ('compte',)
	list_editable = ()



admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(ProfilePro,ProfileProAdmin)
admin.site.register(Releve, releveAdmin)