# blog/views.py
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import CustomUserCreationForm, UserProfileForm, ProfileForm
from .models import Post, Profile


# -------------------------
# Blog Post Views (CRUD)
# -------------------------

# List all posts
class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]


# View a single post
class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"


# Create a new post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


# Update an existing post
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    fields = ["title", "content"]

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# Delete a post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


# -------------------------
# Authentication & Profile Views
# -------------------------

def home(request):
    """Display the homepage"""
    return render(request, "blog/base.html")


def register(request):
    """Handle user registration"""
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                f"Welcome, {user.username}! Your account has been created."
            )
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    """View & edit user + profile details"""
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profile")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)

    return render(
        request,
        "blog/profile.html",
        {"user_form": user_form, "profile_form": profile_form},
    )
