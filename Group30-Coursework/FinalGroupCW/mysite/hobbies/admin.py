from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from hobbies.models import extendedUser, User, Hobby, FriendRequest
from .forms import LoginForm, SignUpForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField


@admin.register(Hobby)
class HobbyAdmin(admin.ModelAdmin):
    list_display = ['id','name']

@admin.register(FriendRequest)
class FRAdmin(admin.ModelAdmin):
    list_display = ['sender','receiver','are_friends']

#admin.site.register(User, UserAdmin)
class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'dob', 'city')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label=("Password"),
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = User
        fields = ('username', 'password','email', 'city', 'dob',)





class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('id','username','email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)


    fieldsets = (
        (None, {'fields': ('username','email', 'password', 'city','dob', 'hobbies', 'profile_pic')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password' , 'city','dob', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(User, CustomUserAdmin)
