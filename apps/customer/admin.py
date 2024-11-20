from django.contrib import admin
from django import forms
from customer.models import User, Profile

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput(attrs={'size': '40'}),
            'get_full_name': forms.TextInput(attrs={'size': '40'}),
        }

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('email', 'get_full_name', 'is_staff', 'is_active', 'is_blacklisted')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    search_fields = ('email',)
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('email',)
        return self.readonly_fields

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__email',)
    readonly_fields = ('created_at', 'updated_at')

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return self.readonly_fields

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)