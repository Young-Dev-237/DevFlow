from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    """
    Modèle d'équipe : regroupe les membres et un responsable (chef d'équipe).
    Conçu en coordination avec Elvira et Elvado.
    """
    name = models.CharField(max_length=150, verbose_name="Nom de l'équipe")
    description = models.TextField(blank=True, verbose_name="Description")
    leader = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='led_teams',
        verbose_name="Chef d'équipe"
    )
    members = models.ManyToManyField(
        User,
        related_name='teams',
        blank=True,
        verbose_name="Membres"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Équipe"
        verbose_name_plural = "Équipes"
        ordering = ['name']

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Profil complémentaire de l'utilisateur (rôle métier et avatar).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=100, default="Développeur", verbose_name="Rôle")
    avatar = models.URLField(blank=True, verbose_name="URL de l'avatar")

    def __str__(self):
        return f"{self.user.username} ({self.role})"
