import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowLeft, Construction } from 'lucide-react';

interface PlaceholderPageProps {
  title: string;
  assignedTo: string;
  description: string;
}

export const PlaceholderPage: React.FC<PlaceholderPageProps> = ({
  title,
  assignedTo,
  description,
}) => {
  return (
    <div className="page-container">
      <Link
        to="/dashboard"
        className="card-action-link"
        style={{ marginBottom: '1rem', display: 'inline-flex' }}
      >
        <ArrowLeft size={16} /> Retour au Tableau de bord
      </Link>
      <div className="page-heading">
        <h1 className="page-title">{title}</h1>
        <p className="page-subtitle">Assigné à : <strong>{assignedTo}</strong></p>
      </div>

      <div className="content-card" style={{ textAlign: 'center', padding: '3.5rem 2rem' }}>
        <div
          style={{
            width: 56,
            height: 56,
            borderRadius: '50%',
            backgroundColor: '#eff6ff',
            color: '#2563eb',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 1.25rem auto',
          }}
        >
          <Construction size={28} />
        </div>
        <h2 style={{ fontSize: '1.25rem', fontWeight: 600, color: 'var(--text-main)', marginBottom: '0.5rem' }}>
          Module en cours de développement
        </h2>
        <p style={{ color: 'var(--text-muted)', maxWidth: 450, margin: '0 auto 1.5rem auto', fontSize: '0.9rem' }}>
          {description}
        </p>
        <Link to="/dashboard" className="btn-primary" style={{ textDecoration: 'none', margin: '0 auto' }}>
          Retourner au Tableau de bord (Ariane)
        </Link>
      </div>
    </div>
  );
};
