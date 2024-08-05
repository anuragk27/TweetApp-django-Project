from django.shortcuts import render
from .models import Blog 
from .forms import BlogForm , UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
# Create your views here.

# Blog List
def blog_list(request): 
    blogs = Blog.objects.all().order_by('-created_at')
    return render(request, 'blog_list.html',{'blogs':blogs})

# Create Blog
@login_required
def blog_create(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request,'blog_form.html',{'form':form})

# Edit Blog
@login_required
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user = request.user)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
            return redirect("blog_list")
    else:
        form = BlogForm(instance=blog)
    return render(request,'blog_form.html',{'form':form})

#Delete Blog
@login_required
def blog_delete(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id, user =request.user)
    if request.method == "POST":
        blog.delete()
        return redirect('blog_list')
    return render(request,'blog_confirm_delete.html',{'blog':blog})

# Register
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            login(request, user)
            return redirect('blog_list')
    else:
        form = UserRegistrationForm()

    return render(request,'registration/register.html',{'form':form})