from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class TaskStatus(models.TextChoices):
    A_FAIRE = 'a_faire', 'À faire'
    EN_COURS = 'en_cours', 'En cours'
    TERMINEE = 'terminee', 'Terminée'

class TaskPriority(models.TextChoices):
    HAUTE = 'haute', 'Haute'
    MOYENNE = 'moyenne', 'Moyenne'
    FAIBLE = 'faible', 'Faible'

class Task(models.Model):
    """
    Modèle Tâche : associé à un projet et attribué à un collaborateur.
    """
    title = models.CharField(max_length=200, verbose_name="Titre")
    description = models.TextField(blank=True, verbose_name="Description")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='tasks',
        verbose_name="Projet associé"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_tasks',
        verbose_name="Assigné à"
    )
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.A_FAIRE,
        verbose_name="Statut"
    )
    priority = models.CharField(
        max_length=20,
        choices=TaskPriority.choices,
        default=TaskPriority.MOYENNE,
        verbose_name="Priorité"
    )
    due_date = models.DateField(null=True, blank=True, verbose_name="Date limite")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tâche"
        verbose_name_plural = "Tâches"
        ordering = ['due_date', '-priority']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
