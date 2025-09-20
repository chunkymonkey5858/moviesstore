from django.contrib import admin
from .models import Movie, Review, Petition, PetitionVote

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

class PetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'movie_title', 'creator', 'yes_votes', 'no_votes', 'created_at']
    list_filter = ['created_at', 'creator']
    search_fields = ['title', 'movie_title', 'description']
    ordering = ['-created_at']

class PetitionVoteAdmin(admin.ModelAdmin):
    list_display = ['user', 'petition', 'vote', 'created_at']
    list_filter = ['vote', 'created_at']
    search_fields = ['user__username', 'petition__title']

admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Petition, PetitionAdmin)
admin.site.register(PetitionVote, PetitionVoteAdmin)
# Register your models here.
