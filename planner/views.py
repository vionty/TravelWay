from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import (
    RegistrationForm,
    PasswordResetUsernameForm,
    TripForm,
    DestinationForm,
    PlaceForm
)
from .models import Trip, Destination, Place


@login_required
def home(request):
    trips = Trip.objects.filter(
        user=request.user
    ).prefetch_related(
        'destinations__places'
    ).annotate(
        destinations_count=Count(
            'destinations',
            distinct=True
        ),
        places_count=Count(
            'destinations__places',
            distinct=True
        )
    ).order_by('-start_date')

    search = request.GET.get('search', '')
    status = request.GET.get('status', '')

    if search:
        trips = trips.filter(
            Q(title__icontains=search) |
            Q(destinations__country__icontains=search) |
            Q(destinations__city__icontains=search)
        ).distinct()

    if status:
        trips = trips.filter(status=status)

    return render(request, 'planner/home.html', {
        'trips': trips,
        'search': search,
        'status': status
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return redirect('home')
    else:
        form = RegistrationForm()

    return render(request, 'registration/register.html', {
        'form': form
    })


def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetUsernameForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']

            try:
                user = User.objects.get(
                    username=username
                )
            except User.DoesNotExist:
                user = None

            if user and user.email:
                uid = urlsafe_base64_encode(
                    force_bytes(user.pk)
                )

                token = default_token_generator.make_token(
                    user
                )

                reset_url = request.build_absolute_uri(
                    reverse(
                        'password_reset_confirm',
                        kwargs={
                            'uidb64': uid,
                            'token': token
                        }
                    )
                )

                send_mail(
                    subject='Восстановление пароля – TravelWay',
                    message=(
                        'Здравствуйте!\n\n'
                        'Вы запросили восстановление пароля '
                        'для аккаунта TravelWay.\n\n'
                        'Перейдите по ссылке, чтобы установить '
                        'новый пароль:\n\n'
                        f'{reset_url}\n\n'
                        'Если вы не запрашивали восстановление '
                        'пароля, просто проигнорируйте это письмо.'
                    ),
                    from_email='noreply@travelway.local',
                    recipient_list=[user.email],
                    fail_silently=False
                )

            return redirect(
                'password_reset_done'
            )

    else:
        form = PasswordResetUsernameForm()

    return render(
        request,
        'registration/password_reset.html',
        {
            'form': form
        }
    )


@login_required
def trip_create(request):
    if request.method == 'POST':
        form = TripForm(request.POST)

        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()

            return redirect(
                'trip_detail',
                trip_id=trip.id
            )
    else:
        form = TripForm()

    return render(request, 'planner/trip_form.html', {
        'form': form,
        'title': 'Новая поездка'
    })


@login_required
def trip_detail(request, trip_id):
    trip = get_object_or_404(
        Trip.objects.prefetch_related(
            'destinations__places'
        ),
        id=trip_id,
        user=request.user
    )

    return render(request, 'planner/trip_detail.html', {
        'trip': trip
    })


@login_required
def trip_edit(request, trip_id):
    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user
    )

    if request.method == 'POST':
        form = TripForm(
            request.POST,
            instance=trip
        )

        if form.is_valid():
            form.save()

            return redirect(
                'trip_detail',
                trip_id=trip.id
            )
    else:
        form = TripForm(instance=trip)

    return render(request, 'planner/trip_form.html', {
        'form': form,
        'title': 'Редактирование поездки'
    })


@login_required
def trip_delete(request, trip_id):
    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user
    )

    if request.method == 'POST':
        trip.delete()
        return redirect('home')

    return render(request, 'planner/trip_confirm_delete.html', {
        'trip': trip
    })


@login_required
def destination_create(request, trip_id):
    trip = get_object_or_404(
        Trip,
        id=trip_id,
        user=request.user
    )

    if request.method == 'POST':
        form = DestinationForm(request.POST)

        if form.is_valid():
            destination = form.save(commit=False)
            destination.trip = trip
            destination.save()

            return redirect(
                'trip_detail',
                trip_id=trip.id
            )
    else:
        form = DestinationForm()

    return render(request, 'planner/destination_form.html', {
        'form': form,
        'trip': trip,
        'title': 'Добавить направление'
    })


@login_required
def destination_edit(request, destination_id):
    destination = get_object_or_404(
        Destination,
        id=destination_id,
        trip__user=request.user
    )

    if request.method == 'POST':
        form = DestinationForm(
            request.POST,
            instance=destination
        )

        if form.is_valid():
            form.save()

            return redirect(
                'trip_detail',
                trip_id=destination.trip.id
            )
    else:
        form = DestinationForm(
            instance=destination
        )

    return render(request, 'planner/destination_form.html', {
        'form': form,
        'trip': destination.trip,
        'title': 'Редактировать направление'
    })


@login_required
def destination_delete(request, destination_id):
    destination = get_object_or_404(
        Destination,
        id=destination_id,
        trip__user=request.user
    )

    trip_id = destination.trip.id

    if request.method == 'POST':
        destination.delete()

        return redirect(
            'trip_detail',
            trip_id=trip_id
        )

    return render(
        request,
        'planner/destination_confirm_delete.html',
        {
            'destination': destination
        }
    )


@login_required
def place_create(request, destination_id):
    destination = get_object_or_404(
        Destination,
        id=destination_id,
        trip__user=request.user
    )

    if request.method == 'POST':
        form = PlaceForm(request.POST)

        if form.is_valid():
            place = form.save(commit=False)
            place.destination = destination
            place.save()

            return redirect(
                'trip_detail',
                trip_id=destination.trip.id
            )
    else:
        form = PlaceForm()

    return render(request, 'planner/place_form.html', {
        'form': form,
        'destination': destination,
        'trip': destination.trip,
        'title': 'Добавить место'
    })


@login_required
def place_edit(request, place_id):
    place = get_object_or_404(
        Place,
        id=place_id,
        destination__trip__user=request.user
    )

    if request.method == 'POST':
        form = PlaceForm(
            request.POST,
            instance=place
        )

        if form.is_valid():
            form.save()

            return redirect(
                'trip_detail',
                trip_id=place.destination.trip.id
            )
    else:
        form = PlaceForm(
            instance=place
        )

    return render(request, 'planner/place_form.html', {
        'form': form,
        'destination': place.destination,
        'trip': place.destination.trip,
        'title': 'Редактировать место'
    })


@login_required
def place_delete(request, place_id):
    place = get_object_or_404(
        Place,
        id=place_id,
        destination__trip__user=request.user
    )

    trip_id = place.destination.trip.id

    if request.method == 'POST':
        place.delete()

        return redirect(
            'trip_detail',
            trip_id=trip_id
        )

    return render(request, 'planner/place_confirm_delete.html', {
        'place': place
    })


@login_required
def place_toggle_visited(request, place_id):
    place = get_object_or_404(
        Place,
        id=place_id,
        destination__trip__user=request.user
    )

    if request.method == 'POST':
        place.visited = not place.visited
        place.save()

    return redirect(
        'trip_detail',
        trip_id=place.destination.trip.id
    )
