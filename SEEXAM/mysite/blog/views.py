from django.shortcuts import render, get_object_or_404
from .models import Post
def post_list(request):
 posts = Post.published.all()
 return render(request,
 'blog/post/list.html',
 {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post,
                             id=id,
                             status=Post.Status.PUBLISHED)

    return render(request,
'blog/post/detail.html',
{'post': post})


def esexam_list(request):
    exams = esexam.objects.filter(is_public=True)  # Только опубликованные

    context = {
        'exams': exams,
        'student_info': "Степанова Екатерина Александровна, группа 241-672"
    }
    return render(request, 'blog/esexam_list.html', context)