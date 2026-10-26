import React from 'react';
import { Link } from 'react-router-dom';
import type { ProjectSummary } from '../../types/dashboard';
import { FolderGit2, Briefcase } from 'lucide-react';

interface MyProjectsProps {
  projects: ProjectSummary[];
}

export const MyProjects: React.FC<MyProjectsProps> = ({ projects }) => {

  const getStatusLabel = (status: ProjectSummary['status']) => {
    switch (status) {
      case 'en_cours':
        return 'En cours';
      case 'en_attente':
        return 'En attente';
      case 'termine':
        return 'Terminé';
      default:
        return status;
    }
  };

  return (
    <div className="content-card">
      <div className="content-card-header">
        <h2 className="card-title">
          <FolderGit2 size={18} color="#2563eb" />
          Mes projets
        </h2>
        {/* Redirige vers la liste complète des projets développée par Daniel */}
        <Link to="/projects" className="card-action-link">
          Voir tout
        </Link>
      </div>

      {projects.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">
            <Briefcase size={24} />
          </div>
          <h3 className="empty-state-title">Aucun projet trouvé</h3>
          <p className="empty-state-desc">
            Vous ne faites actuellement partie d'aucun projet. Créez un projet ou rejoignez une équipe.
          </p>
        </div>
      ) : (
        <div className="projects-list">
          {projects.map((proj) => (
            // Redirige vers la fiche détaillée du projet développée par Daniel
            <Link
              key={proj.id}
              to={`/projects/${proj.id}`}
              className="project-item"
            >
              <div className="project-left">
                <div className="project-icon-box">
                  <FolderGit2 size={16} />
                </div>
                <span className="project-name">{proj.name}</span>
              </div>
              <span className={`badge-status ${proj.status}`}>
                {getStatusLabel(proj.status)}
              </span>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
};
