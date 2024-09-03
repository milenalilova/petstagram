from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from petstagram.common.models import Like
from petstagram.photos.models import Photo


def apply_likes_count(photo):
    photo.likes_count = photo.like_set.count()
    return photo


def apply_user_liked_photos(photo):
    photo.is_liked_by_user = photo.likes_count > 0
    return photo


def index(request):
    search_form = SearchForm(request.GET)
    search_pattern = None
    if search_form.is_valid():
        search_pattern = search_form.cleaned_data['pet_name']

    all_photos = Photo.objects.all()
    if search_pattern:
        all_photos = all_photos.filter(tagged_pets__name__icontains=search_pattern)

    all_photos = [apply_likes_count(photo) for photo in all_photos]
    all_photos = [apply_user_liked_photos(photo) for photo in all_photos]
    comment_form = CommentForm()
    search_form = SearchForm()

    context = {'all_photos': all_photos, 'comment_form': comment_form, 'search_form': search_form}

    return render(request, 'common/home-page.html', context)


def get_user_liked_photo(photo_id):
    return Like.objects.filter(to_photo_id=photo_id)


def like_photo(request, photo_id):
    user_liked_photo = get_user_liked_photo(photo_id)
    if user_liked_photo:
        user_liked_photo.delete()
    else:
        Like.objects.create(to_photo_id=photo_id)

    redirect_path = request.META['HTTP_REFERER'] + f'#{photo_id}'
    return redirect(redirect_path)


def share_photo(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('details photo', photo_id))

    redirect_path = request.META['HTTP_REFERER'] + f'#{photo_id}'
    return redirect(redirect_path)


def add_comment(request, photo_id):
    if request.method == 'POST':
        photo = Photo.objects.get(id=photo_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.to_photo = photo
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')
