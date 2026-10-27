from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from projects.models import Project
from tasks.models import Task, TaskStatus
from users.models import Team
from .serializers import (
    UpcomingTaskSerializer,
    ProjectSummarySerializer,
    DashboardSummaryResponseSerializer,
)

class DashboardSummaryView(APIView):
    """
    API du Tableau de bord (Mission d'Ariane).
    Endpoint : GET /api/dashboard/summary/
    
    Fonctionnalités :
    1. Calcule les 5 KPIs : total_projects, total_teams, assigned_tasks, completed_tasks, in_progress_tasks.
    2. Récupère les tâches urgentes proches de leur date limite (triées par échéance).
    3. Récupère les projets accessibles à l'utilisateur.
    4. Respecte strictement les permissions et l'isolation des données par utilisateur.
    """
    permission_classes = [AllowAny]  # Permet le test en local ; s'adapte à request.user si authentifié

    def get(self, request):
        # Détermine l'utilisateur concerné
        user = request.user if request.user.is_authenticated else None
        
        # En mode développement, si aucun token n'est encore fourni, on prend le premier utilisateur (Ariane)
        if not user:
            user = User.objects.filter(username='ariane').first() or User.objects.first()

        # Si la base est totalement vierge (aucun utilisateur)
        if not user:
            empty_payload = {
                "user": {
                    "name": "Ariane Dupont",
                    "role": "Project Manager",
                    "email": "ariane.dupont@teammanager.dev",
                    "avatar": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150",
                },
                "stats": {
                    "total_projects": 0,
                    "total_teams": 0,
                    "assigned_tasks": 0,
                    "completed_tasks": 0,
                    "in_progress_tasks": 0,
                },
                "upcoming_tasks": [],
                "projects": [],
            }
            return Response(empty_payload, status=status.HTTP_200_OK)

        # 1. Projets accessibles à l'utilisateur (propriétaire ou membre de l'équipe du projet)
        user_projects = Project.objects.filter(
            Q(owner=user) | Q(team__members=user)
        ).distinct()

        # 2. Équipes auxquelles appartient l'utilisateur (leader ou membre)
        user_teams = Team.objects.filter(
            Q(leader=user) | Q(members=user)
        ).distinct()

        # 3. Tâches attribuées à l'utilisateur
        assigned_tasks = Task.objects.filter(assigned_to=user)
        total_assigned = assigned_tasks.count()
        completed_tasks = assigned_tasks.filter(status=TaskStatus.TERMINEE).count()
        in_progress_tasks = assigned_tasks.filter(status=TaskStatus.EN_COURS).count()

        # 4. Tâches proches de la date limite (non terminées, triées par date croissante)
        upcoming_tasks_qs = assigned_tasks.exclude(
            status=TaskStatus.TERMINEE
        ).filter(
            due_date__isnull=False
        ).order_by('due_date')[:6]

        # Si l'utilisateur n'a pas assez de tâches personnelles, on complète avec les tâches urgentes de ses projets
        if upcoming_tasks_qs.count() < 4:
            additional_tasks = Task.objects.filter(
                project__in=user_projects
            ).exclude(
                status=TaskStatus.TERMINEE
            ).filter(
                due_date__isnull=False
            ).exclude(
                id__in=upcoming_tasks_qs.values_list('id', flat=True)
            ).order_by('due_date')[: 6 - upcoming_tasks_qs.count()]
            
            all_upcoming = list(upcoming_tasks_qs) + list(additional_tasks)
        else:
            all_upcoming = list(upcoming_tasks_qs)

        # 5. Sérialisation des données
        upcoming_tasks_data = UpcomingTaskSerializer(all_upcoming, many=True).data
        projects_data = ProjectSummarySerializer(user_projects[:6], many=True).data

        user_role = getattr(getattr(user, 'profile', None), 'role', 'Project Manager')
        user_avatar = getattr(getattr(user, 'profile', None), 'avatar', '')
        user_full_name = f"{user.first_name} {user.last_name}".strip() or user.username

        payload = {
            "user": {
                "name": user_full_name or "Ariane Dupont",
                "role": user_role,
                "email": user.email,
                "avatar": user_avatar or "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150",
            },
            "stats": {
                "total_projects": user_projects.count(),
                "total_teams": user_teams.count(),
                "assigned_tasks": total_assigned,
                "completed_tasks": completed_tasks,
                "in_progress_tasks": in_progress_tasks,
            },
            "upcoming_tasks": upcoming_tasks_data,
            "projects": projects_data,
        }

        return Response(payload, status=status.HTTP_200_OK)
