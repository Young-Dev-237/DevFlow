import React, { useEffect, useState } from 'react';
import {
  FolderGit2,
  Users2,
  CheckSquare2,
  CheckCircle2,
  Clock,
} from 'lucide-react';
import { StatCard } from '../components/dashboard/StatCard';
import { UpcomingTasks } from '../components/dashboard/UpcomingTasks';
import { MyProjects } from '../components/dashboard/MyProjects';
import { LoadingSkeleton } from '../components/dashboard/LoadingSkeleton';
import {
  fetchDashboardSummary,
  MOCK_DASHBOARD_DATA,
} from '../services/dashboardService';
import type { DashboardSummaryResponse } from '../types/dashboard';

interface DashboardPageProps {
  onUserDataLoaded?: (user: DashboardSummaryResponse['user']) => void;
}

export const DashboardPage: React.FC<DashboardPageProps> = ({ onUserDataLoaded }) => {
  const [data, setData] = useState<DashboardSummaryResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Charge les données du dashboard au montage du composant
  const loadData = async () => {
    setLoading(true);
    try {
      // Appelle l'endpoint Django /api/dashboard/summary/
      const res = await fetchDashboardSummary();
      setData(res.data);
      if (onUserDataLoaded) {
        onUserDataLoaded(res.data.user);
      }
    } catch (err) {
      // Si le backend n'est pas encore démarré, on affiche les données de démo conformes à la maquette
      console.warn('Backend non joignable, affichage des données locales :', err);
      setData(MOCK_DASHBOARD_DATA);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  // Permet à l'utilisateur de cocher/décocher une tâche urgente directement depuis le dashboard
  const handleToggleTask = (taskId: string | number) => {
    if (!data) return;

    setData((prev) => {
      if (!prev) return prev;

      const updatedTasks = prev.upcoming_tasks.map((task) => {
        if (task.id === taskId) {
          const newStatus = task.status === 'terminee' ? 'en_cours' : 'terminee';
          return { ...task, status: newStatus as any };
        }
        return task;
      });

      const targetTask = updatedTasks.find((t) => t.id === taskId);
      const isNowCompleted = targetTask?.status === 'terminee';

      // Met à jour les compteurs de statistiques en conséquence
      return {
        ...prev,
        upcoming_tasks: updatedTasks,
        stats: {
          ...prev.stats,
          completed_tasks: prev.stats.completed_tasks + (isNowCompleted ? 1 : -1),
          in_progress_tasks: prev.stats.in_progress_tasks + (isNowCompleted ? -1 : 1),
        },
      };
    });
  };

  return (
    <div className="page-container">
      <div className="page-heading">
        <h1 className="page-title">Tableau de bord</h1>
        <p className="page-subtitle">Vue d'ensemble de votre activité</p>
      </div>

      {loading || !data ? (
        <LoadingSkeleton />
      ) : (
        <>
          {/* Les 5 cartes KPI résumant l'activité */}
          <section className="stats-grid" aria-label="Statistiques principales">
            <StatCard
              label="Projets"
              value={data.stats.total_projects}
              icon={<FolderGit2 size={22} />}
              theme="blue"
            />
            <StatCard
              label="Équipes"
              value={data.stats.total_teams}
              icon={<Users2 size={22} />}
              theme="purple"
            />
            <StatCard
              label="Tâches attribuées"
              value={data.stats.assigned_tasks}
              icon={<CheckSquare2 size={22} />}
              theme="emerald"
            />
            <StatCard
              label="Tâches terminées"
              value={data.stats.completed_tasks}
              icon={<CheckCircle2 size={22} />}
              theme="green"
            />
            <StatCard
              label="Tâches en cours"
              value={data.stats.in_progress_tasks}
              icon={<Clock size={22} />}
              theme="amber"
            />
          </section>

          {/* Deux colonnes : tâches urgentes à gauche, projets récents à droite */}
          <div className="dashboard-content-split">
            <UpcomingTasks
              tasks={data.upcoming_tasks}
              onToggleTask={handleToggleTask}
            />

            <MyProjects projects={data.projects} />
          </div>
        </>
      )}
    </div>
  );
};
