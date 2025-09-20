from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
# Create your models here.
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class Petition(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    movie_title = models.CharField(max_length=255, help_text="Title of the movie you want to see added")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_petitions')
    created_at = models.DateTimeField(auto_now_add=True)
    yes_votes = models.PositiveIntegerField(default=0)
    no_votes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"{self.title} - {self.movie_title}"
    
    def total_votes(self):
        return self.yes_votes + self.no_votes

class PetitionVote(models.Model):
    VOTE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.CharField(max_length=3, choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('petition', 'user')  # One vote per user per petition
    
    def __str__(self):
        return f"{self.user.username} voted {self.vote} on {self.petition.title}"