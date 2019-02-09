from django.urls import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.db import models as models
from django_extensions.db import fields as extension_fields
from . import utils
import qrcode


class Event(models.Model):
    PARTICIPATION_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('team', 'Team')
    )
    EVENT_TYPE_CHOICES = (
        ('technical', 'Technical'),
        ('non-technical', 'Non-Technical')
    )
    name = models.CharField(
        max_length=100,
        blank=True, null=True
    )
    short_description = models.CharField(
        max_length=1000,
        blank=True, null=True
    )
    description = models.TextField(
        blank=True, null=True
    )
    event_type = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=EVENT_TYPE_CHOICES
    )
    fee = models.IntegerField(
        default=50
    )
    participation_type = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=PARTICIPATION_TYPE_CHOICES
    )
    max_participation_in_team = models.IntegerField(
        blank=True, null=True
    )
    total_participants = models.IntegerField(
        default=0
    )
    leader1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leader1"
    )
    leader2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leader2"
    )
    coordinators = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="coordinators"
    )

    class Meta:
        ordering = ('-pk',)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('events_event_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('events_event_update', args=(self.pk,))


class Participant(models.Model):
    UNIVERSITY_CHOICES = (
        ('gtu', 'Gujarat Technological University'),
        ('marwadi', 'Marwadi University'),
        ('atmiya', 'Atmiya University'),
        ('rk', 'RK University'),
        ('others', 'Others')
    )
    name = models.CharField(
        max_length=50,
        blank=True, null=True
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name="event"
    )
    participation_code = models.CharField(
        max_length=4,
        blank=True, null=True
    )
    university = models.CharField(
        max_length=50,
        blank=True, null=True,
        choices=UNIVERSITY_CHOICES
    )
    enrolment_number = models.CharField(
        max_length=50,
        blank=True, null=True
    )
    college = models.CharField(
        max_length=100,
        blank=True, null=True
    )
    phone_number = models.CharField(
        max_length=10,
        blank=True, null=True
    )
    email_id = models.EmailField(
        max_length=254,
        blank=True, null=True
        )
    participated = models.NullBooleanField()
    winner = models.NullBooleanField()
    place_secured = models.IntegerField(
        blank=True, null=True
    )
    campaigner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="campaigner"
    )

    class Meta:
        ordering = ('-pk',)


    def __str__(self):
        return "{} - {}".format(self.name, self.event)

    def __unicode__(self):
        return "{} - {}".format(self.name, self.event)

    def get_absolute_url(self):
        return reverse('events_participant_detail', args=(self.pk,))

    def get_update_url(self):
        return reverse('events_participant_update', args=(self.pk,))


def pre_save_create_participation_code(sender, instance, *args, **kwargs):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    participation_code_g = utils.generate_participation_code()
    culprit = Participant.objects.filter(
        participation_code=participation_code_g
    )
    if not instance.participation_code:
        while culprit:
            participation_code_g = utils.generate_participation_code()
        instance.participation_code = participation_code_g

    qr.add_data(participation_code_g)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save("qrcodes/{}_{}.png".format(
        instance.event.name, participation_code_g
        )
    )


pre_save.connect(pre_save_create_participation_code, sender=Participant)
