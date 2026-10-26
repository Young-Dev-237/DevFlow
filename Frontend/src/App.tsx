import { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { Sidebar } from './components/layout/Sidebar';
import { TopHeader } from './components/layout/TopHeader';
import { DashboardPage } from './pages/DashboardPage';
import { PlaceholderPage } from './pages/PlaceholderPage';
import type { DashboardSummaryResponse } from './types/dashboard';

export default function App() {
  // Profil de l'utilisateur connecté affiché dans le header (mis à jour à la connexion ou via l'API)
  const [user, setUser] = useState<DashboardSummaryResponse['user']>({
    name: 'Ariane Dupont',
    role: 'Project Manager',
    avatar: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&q=80&w=150',
  });

  return (
    <BrowserRouter>
      <div className="app-layout">
        <Sidebar />

        <div className="app-main">
          <TopHeader
            userName={user.name}
            userRole={user.role}
            avatarUrl={user.avatar}
          />

          <Routes>
            {/* Redirection par défaut vers le tableau de bord */}
            <Route path="/" element={<Navigate to="/dashboard" replace />} />

            {/* Module Ariane : Tableau de bord */}
            <Route
              path="/dashboard"
              element={<DashboardPage onUserDataLoaded={(u) => setUser(u)} />}
            />

            {/* Module Daniel : Projets (remplacer PlaceholderPage par ProjectsPage une fois codé) */}
            <Route
              path="/projects"
              element={
                <PlaceholderPage
                  title="Gestion des Projets"
                  assignedTo="Daniel"
                  description="Liste de tous les projets, recherche, filtres et bouton de création de projet."
                />
              }
            />
            <Route
              path="/projects/:id"
              element={
                <PlaceholderPage
                  title="Détails du Projet"
                  assignedTo="Daniel"
                  description="Vue détaillée d'un projet spécifique avec son équipe et ses tâches."
                />
              }
            />

            {/* Module Ornella : Équipes et Tâches (remplacer par TeamsPage et TasksPage) */}
            <Route
              path="/teams"
              element={
                <PlaceholderPage
                  title="Gestion des Équipes"
                  assignedTo="Ornella"
                  description="Liste des équipes, détails des membres et gestion des rôles."
                />
              }
            />
            <Route
              path="/tasks"
              element={
                <PlaceholderPage
                  title="Gestion des Tâches"
                  assignedTo="Ornella"
                  description="Liste complète des tâches avec filtres par statut et par responsable."
                />
              }
            />

            {/* Paramètres & compte */}
            <Route
              path="/settings"
              element={
                <PlaceholderPage
                  title="Paramètres"
                  assignedTo="Joyce / Équipe"
                  description="Préférences du compte et configuration de l'espace de travail."
                />
              }
            />

            <Route path="*" element={<Navigate to="/dashboard" replace />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}
