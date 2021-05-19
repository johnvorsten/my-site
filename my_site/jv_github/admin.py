from django.contrib import admin

# Register your models here.
from .models import User, RepositoryShort, Tag

class TagInLine(admin.TabularInline):
    model = Tag
    extra = 3

# Change admin form
class RepositoryShortAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields':['id', 
                            'repo_name',
                            'repo_user',
                            'repo_description',
                            'repo_description_custom',
                            'repo_show',
                            'repo_last_update',
                            ]}),
        ('links', {'fields':['repo_url','repo_svg']})
        ]

    # Display choice inline
    inlines = [TagInLine] 

    # Change list on object view
    list_display = ('repo_name', 'repo_description')

    list_per_page = 100


admin.site.register(User)
admin.site.register(RepositoryShort, RepositoryShortAdmin)