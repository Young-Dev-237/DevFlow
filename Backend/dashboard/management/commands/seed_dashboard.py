from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from users.models import Team, Profile
from projects.models import Project, ProjectStatus
from tasks.models import Task, TaskStatus, TaskPriority

class Command(BaseCommand):
    help = "Peuple la base de données avec les données de démonstration conformes à la maquette n°3 (Ariane Dupont)."

    def handle(self, *args, **options):
        self.stdout.write("Initialisation des données de test pour Team Manager...")

        # 1. Création de l'utilisateur Ariane Dupont
        ariane, created = User.objects.get_or_create(
            username='ariane',
            defaults={
                'first_name': 'Ariane',
                'last_name': 'Dupont',
                'email': 'ariane.dupont@teammanager.dev',
            }
        )
        if created:
            ariane.set_password('DevFlow2026!')
            ariane.save()

        # Profil Ariane
        Profile.objects.update_or_create(
            user=ariane,
            defaults={
                'role': 'Project Manager',
                'avatar': 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150'
            }
        )

        # Autres collaborateurs
        sarah, _ = User.objects.get_or_create(username='sarah', defaults={'first_name': 'Sarah', 'last_name': 'Lopez', 'email': 'sarah@teammanager.dev'})
        thomas, _ = User.objects.get_or_create(username='thomas', defaults={'first_name': 'Thomas', 'last_name': 'Bernard', 'email': 'thomas@teammanager.dev'})
        julien, _ = User.objects.get_or_create(username='julien', defaults={'first_name': 'Julien', 'last_name': 'Petit', 'email': 'julien@teammanager.dev'})

        # 2. Création des 3 Équipes
        team_alpha, _ = Team.objects.get_or_create(name='Équipe Alpha', defaults={'leader': sarah, 'description': 'Équipe Mobile & UI'})
        team_beta, _ = Team.objects.get_or_create(name='Équipe Beta', defaults={'leader': thomas, 'description': 'Équipe Backend & API'})
        team_gamma, _ = Team.objects.get_or_create(name='Équipe Gamma', defaults={'leader': ariane, 'description': 'Équipe Cloud & DevOps'})

        # Ajout des membres (Ariane fait partie des 3 équipes pour avoir 3 équipes au compteur)
        team_alpha.members.add(ariane, sarah)
        team_beta.members.add(ariane, thomas)
        team_gamma.members.add(ariane, julien)

        # 3. Création des 6 Projets accessibles à Ariane
        projects_data = [
            ("Projet Alpha", "Refonte de la nouvelle application mobile", ProjectStatus.EN_COURS, team_alpha),
            ("Projet Beta", "Refonte du site web institutionnel", ProjectStatus.EN_COURS, team_beta),
            ("Projet Gamma", "Amélioration des performances", ProjectStatus.EN_ATTENTE, team_gamma),
            ("Projet Delta", "Migration vers le cloud", ProjectStatus.TERMINE, team_gamma),
            ("Projet Epsilon", "Refonte du système de paiement", ProjectStatus.EN_COURS, team_beta),
            ("Projet Zeta", "Audit de sécurité et conformité", ProjectStatus.EN_ATTENTE, team_alpha),
        ]

        created_projects = []
        for name, desc, status, team in projects_data:
            proj, _ = Project.objects.update_or_create(
                name=name,
                defaults={
                    'description': desc,
                    'status': status,
                    'owner': ariane,
                    'team': team,
                    'start_date': timezone.localdate() - timedelta(days=30),
                    'end_date': timezone.localdate() + timedelta(days=60),
                }
            )
            created_projects.append(proj)

        p_alpha, p_beta, p_gamma, p_delta, p_epsilon, p_zeta = created_projects

        # Nettoyage des anciennes tâches pour idempotence
        Task.objects.filter(assigned_to=ariane).delete()

        today = timezone.localdate()

        # 4. Tâches en cours (4 tâches) dont les tâches urgentes de la maquette
        Task.objects.create(
            title="Finaliser maquette UI",
            description="Ajuster les composants React et les styles CSS pour le rendu final.",
            project=p_alpha,
            assigned_to=ariane,
            status=TaskStatus.EN_COURS,
            priority=TaskPriority.HAUTE,
            due_date=today, # Aujourd'hui
        )
        Task.objects.create(
            title="Développer l'API des projets",
            description="Créer les endpoints REST pour l'application projets.",
            project=p_beta,
            assigned_to=ariane,
            status=TaskStatus.EN_COURS,
            priority=TaskPriority.MOYENNE,
            due_date=today + timedelta(days=1), # Demain
        )
        Task.objects.create(
            title="Tests d'intégration",
            description="Vérifier la communication entre React et Django REST.",
            project=p_gamma,
            assigned_to=ariane,
            status=TaskStatus.EN_COURS,
            priority=TaskPriority.FAIBLE,
            due_date=today + timedelta(days=3),
        )
        Task.objects.create(
            title="Correction des bugs auth",
            description="Résoudre les problèmes de rafraîchissement des tokens.",
            project=p_delta,
            assigned_to=ariane,
            status=TaskStatus.EN_COURS,
            priority=TaskPriority.MOYENNE,
            due_date=today + timedelta(days=5),
        )

        # 5. Tâches terminées (8 tâches) pour obtenir exactement 12 tâches attribuées (8 terminées + 4 en cours)
        completed_task_titles = [
            ("Initialisation du repository GitHub", p_alpha),
            ("Configuration de l'environnement Django", p_beta),
            ("Mise en place de Vite et React 19", p_alpha),
            ("Ébauche du diagramme de classes", p_gamma),
            ("Intégration du thème sombre Navy", p_alpha),
            ("Définition des interfaces TypeScript", p_beta),
            ("Rédaction de la documentation d'architecture", p_delta),
            ("Revue de code des premiers composants", p_epsilon),
        ]

        for title, proj in completed_task_titles:
            Task.objects.create(
                title=title,
                project=proj,
                assigned_to=ariane,
                status=TaskStatus.TERMINEE,
                priority=TaskPriority.FAIBLE,
                due_date=today - timedelta(days=7),
            )

        self.stdout.write(self.style.SUCCESS(
            "Données insérées avec succès :\n"
            f"- 1 utilisateur principal (Ariane Dupont)\n"
            f"- 3 équipes (Équipe Alpha, Beta, Gamma)\n"
            f"- 6 projets (dont 4 affichés sur le dashboard)\n"
            f"- 12 tâches attribuées à Ariane (8 terminées, 4 en cours) conformes à la maquette n°3 !"
        ))
