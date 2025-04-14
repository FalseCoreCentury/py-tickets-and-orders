from django.db import transaction

from db.models import Movie


def get_movies(title: str = None) -> Movie:
    if title:
        return Movie.objects.filter(title__icontains=title)
    return Movie.objects.all()


@transaction.atomic
def create_movie(title: str, description: str, release_date: str) -> Movie:
    movie = Movie(
        title=title,
        description=description,
        release_date=release_date
    )
    movie.save()
    return movie


def get_movie_by_id(movie_id: int) -> Movie:
    return Movie.objects.get(id=movie_id)
