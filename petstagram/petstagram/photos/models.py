from django.core.validators import MinLengthValidator
from django.db import models

from petstagram.pets.models import Pet
from petstagram.photos.validators import validate_file_size


class Photo(models.Model):
    photo = models.ImageField(
        upload_to='pet_photos/',
        validators=[validate_file_size])

    description = models.CharField(
        max_length=300,
        validators=[MinLengthValidator(10)],
        blank=True,
        null=True,
    )

    location = models.CharField(max_length=30)
    date_of_publication = models.DateField(auto_now_add=True)

    tagged_pets = models.ManyToManyField(Pet, blank=True)
