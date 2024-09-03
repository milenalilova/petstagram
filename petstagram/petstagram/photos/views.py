from django.shortcuts import render, redirect

from petstagram.common.forms import CommentForm
from petstagram.photos.forms import PhotoCreateForm, PhotoEditForm, PhotoDeleteForm
from petstagram.photos.models import Photo


def add_photo(request):
    form = PhotoCreateForm()
    if request.method == 'POST':
        form = PhotoCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index')
    context = {'form': form}
    return render(request, 'photos/photo-add-page.html', context)


def details_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    likes = photo.like_set.count()
    comments = photo.comment_set.all()
    comment_form = CommentForm()

    context = {
        'photo': photo,
        'likes': likes,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'photos/photo-details-page.html', context=context)


def edit_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    form = PhotoEditForm(instance=photo)
    if request.method == 'POST':
        form = PhotoEditForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('details photo', pk=pk)

    context = {'photo': photo, 'form': form}

    return render(request, 'photos/photo-edit-page.html', context)


def delete_photo(request, pk):
    photo = Photo.objects.get(pk=pk)
    form = PhotoDeleteForm(instance=photo)
    if request.method == 'POST':
        form = PhotoDeleteForm(request.POST, instance=photo)
        photo.delete()
        return redirect('index')

    context = {'photo': photo, 'form': form}

    return render(request, 'photos/photo-delete-page.html', context)
