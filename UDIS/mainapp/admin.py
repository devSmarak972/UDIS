from .models import usermodel
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Course)
# admin.site.register(usermodel)
admin.site.register(Publication)
admin.site.register(Experience)
admin.site.register(Professor)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Person)
admin.site.register(Transaction)
admin.site.register(Secretary)
admin.site.register(Student)
admin.site.register(Notification)
admin.site.register(Fees)
admin.site.register(FeeTransaction)
admin.site.register(subjectApplication)
admin.site.register(Project)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = usermodel
    list_display = ("email", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff",
         "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email",)
    ordering = ("email",)


admin.site.register(usermodel, CustomUserAdmin)
