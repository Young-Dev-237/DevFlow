// Niveaux de priorité pour les tâches
export type TaskPriority = 'haute' | 'moyenne' | 'faible';

// Statuts d'avancement d'une tâche
export type TaskStatus = 'a_faire' | 'en_cours' | 'terminee';

// Statuts d'un projet
export type ProjectStatus = 'en_cours' | 'en_attente' | 'termine';

// Structure d'une tâche urgente affichée sur le tableau de bord (partagée avec Ornella)
export interface UpcomingTask {
  id: string | number;
  title: string;
  project_name: string;
  due_date: string;
  due_date_label?: string; // Libellé convivial (ex : "Aujourd'hui", "Demain")
  priority: TaskPriority;
  status: TaskStatus;
  assignee?: {
    name: string;
    avatar?: string;
  };
}

// Aperçu synthétique d'un projet sur le tableau de bord (partagé avec Daniel)
export interface ProjectSummary {
  id: string | number;
  name: string;
  description?: string;
  status: ProjectStatus;
  tasks_count?: number;
  members_count?: number;
}

// Les 5 indicateurs clés (KPIs) calculés par le backend
export interface DashboardStats {
  total_projects: number;
  total_teams: number;
  assigned_tasks: number;
  completed_tasks: number;
  in_progress_tasks: number;
}

// Format attendu pour la réponse de l'endpoint Django GET /api/dashboard/summary/
export interface DashboardSummaryResponse {
  user: {
    name: string;
    role: string;
    email?: string;
    avatar?: string;
  };
  stats: DashboardStats;
  upcoming_tasks: UpcomingTask[];
  projects: ProjectSummary[];
}
