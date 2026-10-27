from rest_framework import serializers
from django.utils import timezone
from datetime import date
from tasks.models import Task
from projects.models import Project

class UpcomingTaskSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les tâches urgentes affichées sur le tableau de bord.
    """
    project_name = serializers.CharField(source='project.name', read_only=True)
    due_date_label = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'project_name',
            'due_date',
            'due_date_label',
            'priority',
            'status',
        ]

    def get_due_date_label(self, obj) -> str:
        if not obj.due_date:
            return ""
        today = timezone.localdate()
        diff = (obj.due_date - today).days

        if diff == 0:
            return "Aujourd'hui"
        elif diff == 1:
            return "Demain"
        elif diff == -1:
            return "Hier (En retard)"
        elif diff < -1:
            return f"En retard ({abs(diff)} jours)"
        else:
            # Format jour mois (ex: 12 mai 2025)
            mois = ["janvier", "février", "mars", "avril", "mai", "juin",
                    "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
            return f"{obj.due_date.day} {mois[obj.due_date.month - 1]} {obj.due_date.year}"


class ProjectSummarySerializer(serializers.ModelSerializer):
    """
    Sérialiseur synthétique pour la liste des projets sur le tableau de bord.
    """
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            'id',
            'name',
            'description',
            'status',
            'tasks_count',
        ]

    def get_tasks_count(self, obj) -> int:
        return obj.tasks.count()


class DashboardStatsSerializer(serializers.Serializer):
    """
    Les 5 indicateurs clés (KPIs) calculés pour l'utilisateur.
    """
    total_projects = serializers.IntegerField()
    total_teams = serializers.IntegerField()
    assigned_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    in_progress_tasks = serializers.IntegerField()


class DashboardSummaryResponseSerializer(serializers.Serializer):
    """
    Structure complète de la réponse GET /api/dashboard/summary/
    """
    user = serializers.DictField()
    stats = DashboardStatsSerializer()
    upcoming_tasks = UpcomingTaskSerializer(many=True)
    projects = ProjectSummarySerializer(many=True)
