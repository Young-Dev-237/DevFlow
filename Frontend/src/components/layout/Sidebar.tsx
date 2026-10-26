import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  FolderGit2,
  Users2,
  CheckSquare2,
  Settings,
  LogOut,
} from 'lucide-react';

export const Sidebar: React.FC = () => {
  return (
    <aside className="app-sidebar">
      {/* Brand Logo */}
      <NavLink to="/dashboard" className="sidebar-brand">
        <div className="brand-icon-box">
          <Users2 size={20} strokeWidth={2.4} />
        </div>
        <span className="brand-text">Team Manager</span>
      </NavLink>

      {/* Main Navigation */}
      <nav className="sidebar-nav">
        <NavLink
          to="/dashboard"
          className={({ isActive }) =>
            `sidebar-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <LayoutDashboard size={18} />
          <span>Tableau de bord</span>
        </NavLink>

        <NavLink
          to="/projects"
          className={({ isActive }) =>
            `sidebar-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <FolderGit2 size={18} />
          <span>Projets</span>
          <span className="sidebar-badge">4</span>
        </NavLink>

        <NavLink
          to="/teams"
          className={({ isActive }) =>
            `sidebar-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <Users2 size={18} />
          <span>Équipes</span>
        </NavLink>

        <NavLink
          to="/tasks"
          className={({ isActive }) =>
            `sidebar-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <CheckSquare2 size={18} />
          <span>Tâches</span>
          <span className="sidebar-badge">12</span>
        </NavLink>
      </nav>

      {/* Footer Nav */}
      <div className="sidebar-footer">
        <NavLink
          to="/settings"
          className={({ isActive }) =>
            `sidebar-nav-link ${isActive ? 'active' : ''}`
          }
        >
          <Settings size={18} />
          <span>Paramètres</span>
        </NavLink>

        <button
          type="button"
          className="sidebar-nav-link"
          style={{ background: 'none', border: 'none', width: '100%', cursor: 'pointer' }}
          onClick={() => {
            alert('Déconnexion effectuée.');
          }}
        >
          <LogOut size={18} />
          <span>Déconnexion</span>
        </button>
      </div>
    </aside>
  );
};
