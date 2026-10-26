import { api } from './api';
import type { DashboardSummaryResponse } from '../types/dashboard';

// Données de simulation conformes  (utilisées tant que le backend n'est pas lancé)
export const MOCK_DASHBOARD_DATA: DashboardSummaryResponse = {
  user: {
    name: 'Ariane Dupont',
    role: 'Project Manager',
    email: 'ariane.dupont@teammanager.dev',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150',
  },
  stats: {
    total_projects: 6,
    total_teams: 3,
    assigned_tasks: 12,
    completed_tasks: 8,
    in_progress_tasks: 4,
  },
  upcoming_tasks: [
    {
      id: 1,
      title: 'Finaliser maquette UI',
      project_name: 'Projet Alpha',
      due_date: '2025-05-10',
      due_date_label: "Aujourd'hui",
      priority: 'haute',
      status: 'en_cours',
    },
    {
      id: 2,
      title: "Développer l'API des projets",
      project_name: 'Projet Beta',
      due_date: '2025-05-11',
      due_date_label: 'Demain',
      priority: 'moyenne',
      status: 'en_cours',
    },
    {
      id: 3,
      title: "Tests d'intégration",
      project_name: 'Projet Gamma',
      due_date: '2025-05-12',
      due_date_label: '12 mai 2025',
      priority: 'faible',
      status: 'a_faire',
    },
    {
      id: 4,
      title: 'Correction des bugs auth',
      project_name: 'Projet Delta',
      due_date: '2025-05-15',
      due_date_label: '15 mai 2025',
      priority: 'moyenne',
      status: 'en_cours',
    },
  ],
  projects: [
    {
      id: 1,
      name: 'Projet Alpha',
      description: 'Refonte de la nouvelle application mobile',
      status: 'en_cours',
    },
    {
      id: 2,
      name: 'Projet Beta',
      description: 'Refonte du site web institutionnel',
      status: 'en_cours',
    },
    {
      id: 3,
      name: 'Projet Gamma',
      description: 'Amélioration des performances',
      status: 'en_attente',
    },
    {
      id: 4,
      name: 'Projet Delta',
      description: 'Migration vers le cloud',
      status: 'termine',
    },
  ],
};

// Récupère les données réelles du tableau de bord depuis Django
export const fetchDashboardSummary = async (): Promise<{
  data: DashboardSummaryResponse;
  isFallback: boolean;
}> => {
  try {
    const response = await api.get<DashboardSummaryResponse>('/dashboard/summary/');
    return { data: response.data, isFallback: false };
  } catch {
    // Si l'API Django n'est pas encore disponible, on renvoie les données de démonstration sans planter
    return { data: MOCK_DASHBOARD_DATA, isFallback: true };
  }
};
