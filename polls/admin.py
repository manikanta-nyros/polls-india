from django.contrib import admin
from polls.models import Poll, Choice, Comment, Vote, Ratings
# Register your models here.


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': ['question']}),
        ('Date Information',  {
         'fields': ['pub_date'], 'classes':['collapse']}),
        ('Expired Date',      {'fields': ['expire_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'expire_date',
                    'was_published_recently', 'sort_by_rating')
    list_filter = ['pub_date']
    #list_filter = ['ratings']
    search_fields = ['question']
admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Comment)
admin.site.register(Vote)
admin.site.register(Ratings)
