from django.db import models
from django.core.validators import FileExtensionValidator
from  django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.urls import reverse
from apps.service.utils import unique_slugify


class Post(models.Model):
    """
    Модель постов для нашего блога
    """
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик'),
    )
    title = models.CharField(verbose_name='Название записи', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255, blank=True)
    description = models.TextField(verbose_name='Краткое описание', max_length=500)
    text = models.TextField(verbose_name='Текст записи')
    category = TreeForeignKey(to='Category', on_delete=models.PROTECT, verbose_name='Категория',
                                     related_name='posts', default=1)
    thumbnail = models.ImageField(default='default.jpg',
                             verbose_name='Изображение записи',
                             blank=True,
                             upload_to='images/thumbnails/%Y/%m/%d/',
                             validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'webp', 'jpeg', 'gif'])])
    status = models.CharField(verbose_name='Статус записи', max_length=10, choices=STATUS_OPTIONS, default='published')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts',
                               default=1)
    updater = models.ForeignKey(to=User, verbose_name='Обновил', on_delete=models.SET_NULL, null=True,
                                  related_name='updater_posts', blank=True)
    fixed = models.BooleanField(default=False, verbose_name='Закрепить')

    class Meta:
        db_table = 'blog_post'
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на статью
        """
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        При сохранении генерируем слаг и проверяем на уникальность
        """
        self.slug = unique_slugify(self, self.title, self.slug)
        super().save(*args, **kwargs)



class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """
    title = models.CharField(verbose_name='Название категории', max_length=255)
    slug = models.SlugField(verbose_name='URL категории', max_length=255, blank=True)
    description = models.TextField(verbose_name='Описание категории', max_length=500)
    parent = TreeForeignKey(
        to='self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='children',
        verbose_name='Родительская категория'
    )
    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Название модели в админ панели, таблица с данными
        """
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        db_table = 'app_categories'

    def get_absolute_url(self):
        """
        Получаем прямую ссылку на категорию
        """
        return reverse('post_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        """
        Возвращение заголовка категории
        """
        return self.title




