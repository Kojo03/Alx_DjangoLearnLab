from django.contrib import admin
from .models import Book
from django.contrib.auth.admin import UserAdmin 
from .models import Author, Book, CustomUser
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    list_filter = ('publication_date',)
    search_fields = ('title', 'author')

class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('date_of_birth', 'profile_photo')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

add_fieldsets = (
    (None, {
        'classes': ('wide',),
        'fields': ('username', 'email', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
    }),

)

list_display = ('username', 'email', 'date_of_birth', 'is_active', 'is_staff', 'is_superuser')
search_fields = ('username', 'email')
ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
