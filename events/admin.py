from django.contrib import admin
from django import forms
from .models import Event, Participant


class EventAdminForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ['name', 'participation_type', 'total_participants']


admin.site.register(Event, EventAdmin)


class ParticipantAdminForm(forms.ModelForm):

    class Meta:
        model = Participant
        fields = '__all__'


class ParticipantAdmin(admin.ModelAdmin):
    form = ParticipantAdminForm


admin.site.register(Participant, ParticipantAdmin)
