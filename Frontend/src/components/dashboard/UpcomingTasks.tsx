import React from 'react';
import { Link } from 'react-router-dom';
import type { UpcomingTask } from '../../types/dashboard';
import { Check, Folder, CalendarClock } from 'lucide-react';

interface UpcomingTasksProps {
  tasks: UpcomingTask[];
  onToggleTask?: (taskId: string | number) => void;
}

export const UpcomingTasks: React.FC<UpcomingTasksProps> = ({ tasks, onToggleTask }) => {
  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="card-title">
          <CalendarClock size={18} color="#2563eb" />
          Tâches proches de la date limite
        </h2>
        {/* Redirige vers la page complète des tâches développée par Ornella */}
        <Link to="/tasks" className="card-action-link">
          Voir tout
        </Link>
      </div>

      {tasks.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">
            <Check size={24} />
          </div>
          <h3 className="empty-state-title">Aucune tâche urgente</h3>
          <p className="empty-state-desc">
            Toutes vos tâches proches de l'échéance sont traitées ou aucune date limite n'approche.
          </p>
        </div>
      ) : (
        <div className="tasks-list">
          {tasks.map((task) => {
            const isCompleted = task.status === 'terminee';
            // Met en valeur si la tâche est à rendre aujourd'hui ou demain
            const isUrgent =
              task.due_date_label?.toLowerCase().includes("aujourd'hui") ||
              task.due_date_label?.toLowerCase().includes('demain');

            return (
              <div key={task.id} className="task-item">
                <div className="task-main">
                  {/* Bouton pour cocher rapidement la tâche */}
                  <button
                    type="button"
                    aria-label={`Marquer comme ${isCompleted ? 'à faire' : 'terminée'}`}
                    className={`task-indicator ${isCompleted ? 'completed' : ''}`}
                    onClick={() => onToggleTask && onToggleTask(task.id)}
                  >
                    {isCompleted && <Check size={12} strokeWidth={3} />}
                  </button>

                  <div className="task-details">
                    <span
                      className="task-title"
                      style={{
                        textDecoration: isCompleted ? 'line-through' : 'none',
                        color: isCompleted ? 'var(--text-muted)' : 'var(--text-main)',
                      }}
                    >
                      {task.title}
                    </span>
                    <span className="task-project">
                      <Folder size={12} />
                      {task.project_name}
                    </span>
                  </div>
                </div>

                <div className="task-meta">
                  <span className={`due-date-text ${isUrgent ? 'urgent' : ''}`}>
                    {task.due_date_label || task.due_date}
                  </span>
                  <span className={`badge-priority ${task.priority}`}>
                    {task.priority}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
