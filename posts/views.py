from django.shortcuts import render, get_object_or_404, redirect
from tags.models import Tag
from catalogs.models import Catalog
from django.db.models import Count, Q
from .models import Post, Comment
from .forms import CommentForm

def post_list(request):
    catalogs = request.GET.getlist('catalog')
    tags = request.GET.getlist('tag')
    search = request.GET.get('search', '')
    sort_option = request.GET.get('sort', 'latest')


    posts = Post.objects.annotate(comment_count=Count('comments'))


    if catalogs:
        posts = posts.filter(catalog__id__in=[int(cat) for cat in catalogs if cat.isdigit()])
    if tags:
        posts = posts.filter(tag__id__in=[int(tag) for tag in tags if tag.isdigit()])


    if search:
        posts = posts.filter(Q(name__icontains=search) | Q(description__icontains=search))


    sort_map = {
        'latest': '-created_at',
        'oldest': 'created_at',
        'popular': '-comment_count',
    }
    posts = posts.order_by(sort_map.get(sort_option, '-created_at'))

    ctx = {
        'posts': posts,
        'catalogs': Catalog.objects.all(),
        'tags': Tag.objects.all(),
        'selected_catalogs': catalogs,
        'selected_tags': tags,
        'current_sort': sort_option,
        'search_query': search,
    }
    return render(request,  'posts/index_with_side_bar.html', ctx)

def post_detail(request, year, month, day, slug):
    post = get_object_or_404(Post, slug=slug, created_at__year=year, created_at__month=month, created_at__day=day)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(post.get_detail_url())
    else:
        comment_form = CommentForm()

    comments = post.comments.select_related('post').order_by('-created_at')

    ctx = {
        'post': post,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', ctx)
