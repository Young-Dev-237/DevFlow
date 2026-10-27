from django.db import models
from django.contrib.auth.models import User
from users.models import Team

class ProjectStatus(models.TextChoices):
    EN_COURS = 'en_cours', 'En cours'
    EN_ATTENTE = 'en_attente', 'En attente'
    TERMINE = 'termine', 'Terminé'

class Project(models.Model):
    """
    Modèle Projet : regroupe les tâches et est rattaché à un propriétaire et/ou une équipe.
    """
    name = models.CharField(max_length=200, verbose_name="Nom du projet")
    description = models.TextField(blank=True, verbose_name="Description")
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owned_projects',
        verbose_name="Responsable"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='projects',
        verbose_name="Équipe assignée"
    )
    status = models.CharField(
        max_length=20,
        choices=ProjectStatus.choices,
        default=ProjectStatus.EN_COURS,
        verbose_name="Statut"
    )
    start_date = models.DateField(null=True, blank=True, verbose_name="Date de début")
    end_date = models.DateField(null=True, blank=True, verbose_name="Date de fin")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
