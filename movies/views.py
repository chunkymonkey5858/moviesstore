from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition, PetitionVote
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()
    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html',
                  {'template_data': template_data})
def show(request, id):
    movie =  Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)
    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html',
                  {'template_data': template_data})
@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
    
@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html',
            {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)
# Create your views here.
@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id,
        user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

# Petition views
def petition_list(request):
    petitions = Petition.objects.all().order_by('-created_at')
    template_data = {
        'title': 'Movie Petitions',
        'petitions': petitions
    }
    return render(request, 'movies/petition_list.html', {'template_data': template_data})

@login_required
def petition_detail(request, petition_id):
    petition = get_object_or_404(Petition, id=petition_id)
    user_vote = None
    if request.user.is_authenticated:
        try:
            user_vote = PetitionVote.objects.get(petition=petition, user=request.user)
        except PetitionVote.DoesNotExist:
            pass
    
    template_data = {
        'title': f'Petition: {petition.title}',
        'petition': petition,
        'user_vote': user_vote
    }
    return render(request, 'movies/petition_detail.html', {'template_data': template_data})

@login_required
def petition_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        movie_title = request.POST.get('movie_title')
        
        if title and description and movie_title:
            petition = Petition.objects.create(
                title=title,
                description=description,
                movie_title=movie_title,
                creator=request.user
            )
            messages.success(request, 'Petition created successfully!')
            return redirect('movies.petition_detail', petition_id=petition.id)
        else:
            messages.error(request, 'Please fill in all fields.')
    
    template_data = {
        'title': 'Create New Petition'
    }
    return render(request, 'movies/petition_create.html', {'template_data': template_data})

@login_required
def petition_vote(request, petition_id):
    if request.method == 'POST':
        petition = get_object_or_404(Petition, id=petition_id)
        vote_choice = request.POST.get('vote')
        
        if vote_choice not in ['yes', 'no']:
            messages.error(request, 'Invalid vote choice.')
            return redirect('movies.petition_detail', petition_id=petition_id)
        
        # Check if user already voted
        existing_vote, created = PetitionVote.objects.get_or_create(
            petition=petition,
            user=request.user,
            defaults={'vote': vote_choice}
        )
        
        if not created:
            # User already voted, update their vote
            old_vote = existing_vote.vote
            existing_vote.vote = vote_choice
            existing_vote.save()
            
            # Update vote counts
            if old_vote == 'yes':
                petition.yes_votes -= 1
            else:
                petition.no_votes -= 1
                
            if vote_choice == 'yes':
                petition.yes_votes += 1
            else:
                petition.no_votes += 1
        else:
            # New vote
            if vote_choice == 'yes':
                petition.yes_votes += 1
            else:
                petition.no_votes += 1
        
        petition.save()
        messages.success(request, f'Your vote has been recorded!')
        
    return redirect('movies.petition_detail', petition_id=petition_id)