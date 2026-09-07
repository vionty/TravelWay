from django.contrib import admin

from .models import Trip, Destination, Place


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'start_date',
        'end_date',
        'budget',
        'status',
        'user',
    )

    list_filter = (
        'status',
    )

    search_fields = (
        'title',
        'notes',
    )


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = (
        'country',
        'city',
        'trip',
    )

    list_filter = (
        'country',
    )

    search_fields = (
        'country',
        'city',
    )


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'destination',
        'visited',
    )

    list_filter = (
        'visited',
    )

    search_fields = (
        'name',
        'address',
    )