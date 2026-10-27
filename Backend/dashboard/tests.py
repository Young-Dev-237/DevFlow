from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from rest_framework.test import APIClient
from rest_framework import status

from users.models import Team, Profile
from projects.models import Project, ProjectStatus
from tasks.models import Task, TaskStatus, TaskPriority

class DashboardSummaryAPITestCase(TestCase):
    """
    Tests unitaires pour l'API du Tableau de bord (Ariane).
    Vérifie les calculs de statistiques, les filtres d'échéance et l'isolation des permissions.
    """

    def setUp(self):
        self.client = APIClient()
        self.today = timezone.localdate()

        # Utilisateur 1 : Ariane Dupont
        self.ariane = User.objects.create_user(
            username='ariane',
            email='ariane.dupont@teammanager.dev',
            first_name='Ariane',
            last_name='Dupont'
        )
        Profile.objects.create(user=self.ariane, role='Project Manager')

        # Utilisateur 2 : Autre collaborateur (Charlie)
        self.charlie = User.objects.create_user(
            username='charlie',
            email='charlie@teammanager.dev',
            first_name='Charlie',
            last_name='Dev'
        )
        Profile.objects.create(user=self.charlie, role='Développeur')

        # Équipes d'Ariane
        self.team1 = Team.objects.create(name='Équipe Alpha', leader=self.ariane)
        self.team1.members.add(self.ariane)
        self.team2 = Team.objects.create(name='Équipe Beta', leader=self.ariane)
        self.team2.members.add(self.ariane)

        # Projets d'Ariane
        self.proj1 = Project.objects.create(
            name='Projet Alpha',
            owner=self.ariane,
            team=self.team1,
            status=ProjectStatus.EN_COURS
        )
        self.proj2 = Project.objects.create(
            name='Projet Beta',
            owner=self.ariane,
            team=self.team2,
            status=ProjectStatus.TERMINE
        )

        # Tâches attribuées à Ariane
        # 2 en cours
        self.task1 = Task.objects.create(
            title="Finaliser maquette UI",
            project=self.proj1,
            assigned_to=self.ariane,
            status=TaskStatus.EN_COURS,
            priority=TaskPriority.HAUTE,
            due_date=self.today
        )
        self.task2 = Task.objects.create(
            title="API Projets",
            project=self.proj2,
            assigned_to=self.ariane,
            status=TaskStatus.EN_COURS,
            priority=TaskPriority.MOYENNE,
            due_date=self.today + timedelta(days=2)
        )
        # 1 terminée
        self.task3 = Task.objects.create(
            title="Setup Repo",
            project=self.proj1,
            assigned_to=self.ariane,
            status=TaskStatus.TERMINEE,
            priority=TaskPriority.FAIBLE,
            due_date=self.today - timedelta(days=5)
        )

    def test_dashboard_summary_for_ariane(self):
        """Vérifie le calcul exact des KPIs pour Ariane."""
        self.client.force_authenticate(user=self.ariane)
        response = self.client.get('/api/dashboard/summary/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Vérification du profil
        self.assertEqual(data['user']['name'], 'Ariane Dupont')
        self.assertEqual(data['user']['role'], 'Project Manager')

        # Vérification des statistiques
        self.assertEqual(data['stats']['total_projects'], 2)
        self.assertEqual(data['stats']['total_teams'], 2)
        self.assertEqual(data['stats']['assigned_tasks'], 3)
        self.assertEqual(data['stats']['completed_tasks'], 1)
        self.assertEqual(data['stats']['in_progress_tasks'], 2)

        # Vérification des tâches urgentes (la tâche terminée ne doit pas apparaître)
        upcoming_titles = [t['title'] for t in data['upcoming_tasks']]
        self.assertIn("Finaliser maquette UI", upcoming_titles)
        self.assertIn("API Projets", upcoming_titles)
        self.assertNotIn("Setup Repo", upcoming_titles)

    def test_permissions_isolation_between_users(self):
        """Vérifie que Charlie ne voit pas les projets, équipes ou tâches d'Ariane."""
        self.client.force_authenticate(user=self.charlie)
        response = self.client.get('/api/dashboard/summary/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data

        # Charlie n'a aucun projet, équipe ni tâche
        self.assertEqual(data['stats']['total_projects'], 0)
        self.assertEqual(data['stats']['total_teams'], 0)
        self.assertEqual(data['stats']['assigned_tasks'], 0)
        self.assertEqual(len(data['upcoming_tasks']), 0)
        self.assertEqual(len(data['projects']), 0)
