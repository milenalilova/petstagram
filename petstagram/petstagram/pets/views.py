from django.shortcuts import render, redirect

from petstagram.common.forms import CommentForm
from petstagram.pets.forms import PetAddForm, PetEditForm, PetDeleteForm
from petstagram.pets.models import Pet
from petstagram.photos.models import Photo


def add_pet(request):
    if request.method == 'GET':
        form = PetAddForm
    else:
        form = PetAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('details user', pk=2)

    context = {'form': form}

    return render(request, 'pets/pet-add-page.html', context)


def details_pet(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    all_photos = pet.photo_set.all()
    comment_form = CommentForm()

    context = {
        'pet': pet,
        'all_photos': all_photos,
        'comment_form': comment_form,
    }
    return render(request, 'pets/pet-details-page.html', context)


def edit_pet(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    if request.method == 'GET':
        form = PetEditForm(instance=pet)
    else:
        form = PetEditForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('details pet', username, pet_slug)
    context = {'form': form}

    return render(request, 'pets/pet-edit-page.html', context)


def delete_pet(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    if request.method == 'POST':
        pet.delete()
        return redirect('details user', pk=1)
    form = PetDeleteForm(instance=pet)

    context = {'form': form}

    return render(request, 'pets/pet-delete-page.html', context)
