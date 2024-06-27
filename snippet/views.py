from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate

from snippet.admin import CustomUserCreationForm

from .forms import SnippetForm
from .models import CustomUser, Snippet


@login_required
def snippet_list(request):
    snippets = Snippet.objects.filter(author=request.user)
    return render(request, "snippet/snippet_list.html", {"snippets": snippets})


@login_required
def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, "snippet/snippet_detail.html", {"snippet": snippet})


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("snippet_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


@login_required
def create_snippet(request):
    if request.method == "POST":
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.author = request.user
            snippet.save()
            return redirect("snippet_list")
    else:
        form = SnippetForm()
    return render(request, "snippet/create_snippet.html", {"form": form})

@login_required
def update_profile(request, username):
    user = CustomUser.objects.get(username=username)
    return render(request, "snippet/update_profile.html", {'user': user})