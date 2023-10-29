from django.contrib import admin

from .models import Category, Location, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'pub_date',
        'author',
        'location',
        'is_published',
        'created_at',
        'category'
    )

    list_editable = (
        'is_published',
        'category'
    )

    search_fields = ('title',)
    list_filter = ('category',)
    list_display_links = ('title',)


admin.site.register(Location)
