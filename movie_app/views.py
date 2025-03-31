from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.models import User
from . models import Movie,Review,Category,Favorite
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import update_session_auth_hash

# Create your views here.
def base(request):
    return render(request,'movie/index.html')

def home(request):
    return render(request,"movie/home.html")

def user_register(request):
    if request.method == "POST":
        username=request.POST.get('username')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')  

        
        if not username or not first_name or not last_name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required!")
            return redirect("user_register")

        if User.objects.filter(username=username).exists():
            messages.error(request,"Username Already Exists !! Choose Another One")
            return redirect("user_register")
        if User.objects.filter(email=email).exists():
            messages.error(request,"Email Already Exists !!")
            return redirect("user_register")
        if len(password)<5:
            messages.error(request,"Password must be above 5 letters !!")
            return redirect("user_register")
        if confirm_password != password:
            messages.error(request,"Your password is wrong !!")
            return redirect("user_register")

        user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
        user.save()
        messages.success(request,f"{ user.username } Successfully Register")
        return redirect("user_login")
    else:
        messages.error(request,"Something Went Wrong in registration !!")
    return render(request,"movie/user_register.html")

def user_login(request):
    if request.method== "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")

        user=authenticate(username=username,password=password)
        if  user is not None:
            login(request,user)
            messages.success(request,f"{ user.username } Successfully Login")
            return redirect("home")
        else:
            messages.error(request,"Invalid Username or Password !!")
            return redirect("user_login")
    return render(request,"movie/user_login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out!")
    return redirect("base")


def profile(request):
    user=request.user
    if request.method == "POST":
        if "update_profile" in request.POST:
            if "update_profile" in request.POST:
                new_username = request.POST.get("username", user.username)
                new_first_name = request.POST.get("first_name", user.first_name)
                new_last_name = request.POST.get("last_name", user.last_name)
                new_email = request.POST.get("email", user.email)

            if User.objects.exclude(id=user.id).filter(username=new_username).exists():
                messages.error(request, "Username already taken! Choose another one.")
                return redirect('profile')
            
            if User.objects.exclude(id=user.id).filter(email=new_email).exists():
                messages.error(request, "Email already taken! Use another one.")
                return redirect('profile')

            user.username = new_username
            user.first_name = new_first_name
            user.last_name = new_last_name
            user.email = new_email
            user.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
        
        elif "update_password" in request.POST:
            current_password=request.POST.get("current_password")
            new_password=request.POST.get("new_password")
            confirm_password=request.POST.get("confirm_password")

            if not user.check_password(current_password):
                messages.error(request, "Current password is incorrect!")
            
            elif len(new_password) < 5:
                messages.error(request, "New password must be at least 5 characters!")

            elif new_password != confirm_password:
                messages.error(request, "New passwords do not match!")
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully!")

        return redirect('profile')
    
    return render(request, 'movie/profile.html')

def movie_list(request):
    movies=Movie.objects.all()
    favorite_movies = []
    if request.user.is_authenticated:
        favorite_movies = Favorite.objects.filter(user=request.user).values_list("movie_id", flat=True)

    return render(request,'movie/movie_list.html',{'movies':movies,"favorite_movies": favorite_movies})

def base_movie_list(request):
    movies=Movie.objects.all()
    return render(request,'movie/base_movie_list.html',{'movies':movies})

def movie_detail(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id)
    reviews=Review.objects.filter(movie=movie)
    return render(request, 'movie/movie_detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def add_movie(request):
    if request.method == "POST":
        title=request.POST.get("title")
        poster=request.FILES.get("poster")
        description=request.POST.get("description")
        release_date=request.POST.get("release_date")
        actors=request.POST.get("actors")
        category=Category.objects.get(id=request.POST.get("category"))
        youtube_trailer=request.POST.get("youtube_trailer")
        
        Movie.objects.create(user=request.user,title=title, poster=poster, description=description,release_date=release_date, actors=actors, category=category, youtube_trailer=youtube_trailer)
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'movie/add_movie.html', {'categories': categories})


@login_required
def edit_movie(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id,user=request.user)
    if request.method == "POST":
        movie.title=request.POST.get("title")
        if 'poster' in request.FILES:
            movie.poster=request.FILES.get("poster")
        movie.description=request.POST.get("description")
        movie.release_date=request.POST.get("release_date")
        movie.actors=request.POST.get("actors")
        movie.category = Category.objects.get(id=request.POST.get('category'))
        movie.youtube_trailer = request.POST.get('youtube_trailer')
        movie.save()
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'movie/edit_movie.html', {'movie': movie, 'categories': categories})


@login_required
def delete_movie(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id,user=request.user)
    if movie.user != request.user:
        return redirect('home')
    movie.delete()
    return redirect('home')   

@login_required
def add_review(request,movie_id):
    if request.method == "POST":
        text=request.POST.get("text")
        rating=request.POST.get("rating")

        movie=get_object_or_404(Movie,id=movie_id)
        Review.objects.create(user=request.user,text=text,rating=rating,movie=movie)
    return redirect('movie/movie_detail', movie_id=movie_id)


# def search_movie(request,movie_id):
#     movie=get_object_or_404(Movie,id=movie_id,user=request.user)
#     category=movie.category

#     related_movies=Movie.objects.filter(category=category).exclude(id=movie.id).order_by('-created_at')[:10]

#     return render(request, 'movie_list.html', {'movie': movie, 'related_movies': related_movies})



def search_movie(request):
    query = request.GET.get('q', '').strip() 
    movies = Movie.objects.all()

    if query:
        movies = movies.filter(category__name__icontains=query).order_by('-category')if query else Movie.objects.all()

    return render(request, 'movie/movie_list.html', {'movies': movies, 'query': query})


def favorite_list(request):
    favorites=Favorite.objects.filter(user=request.user).select_related('movie')
    movies=[favorite.movie for favorite in favorites]
    return render(request,"movie/favorite_list.html",{'movies':movies})

def delete_fav_list(request,movie_id):
    favorites=get_object_or_404(Favorite,movie_id=movie_id,user=request.user)
    favorites.delete()
    return redirect('favorite_list')

def toggle_favorite(request,movie_id):
    movie=get_object_or_404(Movie,id=movie_id)
    favorite, created=Favorite.objects.get_or_create(movie=movie,user=request.user)

    if not created:
        favorite.delete()
    return redirect('movie_list')
