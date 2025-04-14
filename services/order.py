from django.utils import timezone

from django.core.exceptions import ObjectDoesNotExist

from db.models import Order, User, MovieSession, Ticket


def create_order(
        tickets: list[dict],
        username: str,
        date: str = None
) -> Order:
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        raise ValueError(f"User with username '{username}' does not exist.")

    created_at = date if date else timezone.now()
    order = Order.objects.create(user=user, created_at=created_at)

    for ticket in tickets:
        try:
            movie_session = MovieSession.objects.get(
                id=ticket["movie_session"]
            )

            Ticket.objects.create(
                order=order,
                movie_session=movie_session,
                row=ticket["row"],
                seat=ticket["seat"],
            )
        except MovieSession.DoesNotExist:
            raise ValueError(
                f"Movie session with id "
                f"'{ticket['movie_session']}' does not exist."
            )

    return order


def get_orders(username: str = None) -> Order:
    if username:
        user = User.objects.get(username=username)
        return Order.objects.filter(user=user)
    return Order.objects.all()
