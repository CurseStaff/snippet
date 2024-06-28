from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from snippet.admin import CustomUserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import CustomUser, languages, Snippet
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy, reverse
from .forms import SnippetForm, UserEditForm
from .models import CustomUser, Snippet

import django_filters

# FilterViews


class SnippetFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains", label="Title"
    )
    language = django_filters.ChoiceFilter(
        field_name="language",
        choices=[language for language in languages],
        lookup_expr="iexact",
        label="Programming Language",
    )

    class Meta:
        model = Snippet
        fields = ["title"]


@login_required
def snippet_filter_list(request):
    f = SnippetFilter(request.GET, queryset=Snippet.objects.all())
    return render(request, "snippet/snippet_filter_list.html", {"filter": f})


# Views


def home(request):
    return render(request, "snippet/home.html")


@login_required
def snippet_list(request):
    snippets = Snippet.objects.filter(author=request.user)
    return render(request, "snippet/snippet_list.html", {"snippets": snippets})


@login_required
def snippet_detail(request, pk):
    snippet = get_object_or_404(Snippet, pk=pk)
    return render(request, "snippet/snippet_detail.html", {"snippet": snippet})


@login_required
def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse("home"))  # Redirect to your home URL name

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
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
    user = get_object_or_404(CustomUser, username=username)

    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile")
    else:
        form = UserEditForm(instance=user)

    return render(request, "snippet/edit_profile.html", {"form": form})


# Custom 404 Handling


def custom_404(request, exception):
    return render(request, "404.html", status=404)


@login_required
def profile(request):
    return render(request, "snippet/profile.html")


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    success_url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.success_url)
        else:
            return super().get(request, *args, **kwargs)
