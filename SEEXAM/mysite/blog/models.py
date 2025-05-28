from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)
    objects = models.Manager()  # default manager
    published = PublishedManager()  # custom manager

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title


class esexam(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='authored_exams',
        verbose_name="Автор",
        null=True)  # Временно)

    title = models.CharField(max_length=250, verbose_name="Exam Title")

    created = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")

    exam_date = models.DateTimeField(verbose_name="Exam Date")
    image = models.ImageField(upload_to='exam_images/',
                              blank=True,
                              null=True,
                              verbose_name="Exam Image")

    users = models.ManyToManyField(User, verbose_name="Assigned Users")

    is_public = models.BooleanField(default=False, verbose_name="Published")

    class Meta:
        ordering = ['-created']
        verbose_name = "Exam"
        verbose_name_plural = "Exams"

    def __str__(self):
        return self.title
