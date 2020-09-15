from django.shortcuts import render, HttpResponse, get_object_or_404, HttpResponseRedirect, redirect, Http404
from .models import Post
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.utils.text import slugify
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.db.models import Q

def post_index(request):
	post_list= Post.objects.all()
	query = request.GET.get('q')
	if query:
		post_list= post_list.filter(
			Q(title__icontains=query) |
			Q(content__icontains = query) |
			Q(user__first_name__icontains=query) |
			Q(user__last_name__icontains=query)
		).distinct()

	paginator = Paginator(post_list, 5)

	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts = paginator.page(1)
	except EmptyPage:
		posts = paginator.page(paginator.num_pages)

	return render(request, 'post/index.html', {'posts': posts})

def post_detail(request,slug):
	post = get_object_or_404(Post,slug=slug)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.post = post
		comment.save()
		return HttpResponseRedirect(post.get_absolute_url())
	context={
	'post': post,
	'form': form,
	}
	return render(request, 'post/detail.html',context)

def post_create(request):

	if not request.user.is_authenticated:
		# Eğer kullanıcı giriş yapmamış ise hata sayfası gönder
		return Http404()

	#Request.post bize metinsel nesneler getirir, request.files bize
	
	form= PostForm()
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		post = form.save(commit=False)
		post.user= request.user
		post.save()
		messages.success(request,'Successfully inserted!!')
		return HttpResponseRedirect(post.get_absolute_url())
	context={
		'form': form,
	}
	return render(request, 'post/form.html',context)
	#if request.method == "POST":
	#	print(request.POST)
	#Aşağıdaki kısım pek tercih edilen bir şey değil o yüzdden PostFormu kullanacağız
	#title = request.POST.get('title')
	#content = request.POST.get('content')
	#Post.objects.create(title=title , content=content)

	#if request.method =="POST":
	#	form = PostForm(request.POST)
	#	if form.is_valid():
	#		form.save()
	#else: 
	#	form = PostForm()

	

def post_update(request, slug):

	if not request.user.is_authenticated:
		return Http404()

	post = get_object_or_404(Post,slug=slug)
	form = PostForm(request.POST or None,request.FILES or None, instance=post )
	if form.is_valid():
		form.save()
		messages.success(request,'Successfully updated!!', extra_tags='mesaj-basarili')
		return redirect(post.get_absolute_url())
	context={
		'form': form,
	}
	return render(request, 'post/form.html',context)
	#extra-tags bizim css sınıfımız bunları düzenlemelerde kullanacağız 

def post_delete(request,slug):

	if not request.user.is_authenticated:
		return Http404()

	post = get_object_or_404(Post,slug=slug)
	post.delete()
	return redirect('post:index')



# Create your views here.
