from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Breed(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Kitten(models.Model):
    breed = models.ForeignKey(Breed, related_name='kittens', on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    age = models.PositiveIntegerField(help_text='Возраст в полных месяцах')
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='kittens', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.breed.name} - {self.color}"
    
    def get_average_rating(self):
        average = self.ratings.aggregate(Avg('score'))['score__avg']
        return average if average is not None else 0

class Rating(models.Model):
    kitten = models.ForeignKey(Kitten, related_name='ratings', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE)
    score = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ('kitten', 'user')

    def __str__(self):
        return f"Rating {self.score} by {self.user.username} for {self.kitten}"
