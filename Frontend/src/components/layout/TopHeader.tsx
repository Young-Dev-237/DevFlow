import React from 'react';
import { Search, Bell } from 'lucide-react';

interface TopHeaderProps {
  userName?: string;
  userRole?: string;
  avatarUrl?: string;
  onSearchChange?: (query: string) => void;
}

export const TopHeader: React.FC<TopHeaderProps> = ({
  userName = 'Ariane Dupont',
  userRole = 'Project Manager',
  avatarUrl,
  onSearchChange,
}) => {
  return (
    <header className="app-header">
      {/* Search Input */}
      <div className="header-search">
        <Search size={16} />
        <input
          type="text"
          placeholder="Rechercher..."
          onChange={(e) => onSearchChange && onSearchChange(e.target.value)}
        />
      </div>

      {/* Right Actions */}
      <div className="header-actions">
        {/* Notifications */}
        <button type="button" className="icon-btn" aria-label="Notifications">
          <Bell size={18} />
          <span className="notification-dot" />
        </button>

        {/* User Profile Widget */}
        <div className="user-profile-widget">
          {avatarUrl ? (
            <img
              src={avatarUrl}
              alt={userName}
              className="user-avatar"
            />
          ) : (
            <div className="user-avatar-fallback">
              {userName
                .split(' ')
                .map((n) => n[0])
                .join('')}
            </div>
          )}
          <div className="user-meta">
            <span className="user-name">{userName}</span>
            <span className="user-role">{userRole}</span>
          </div>
        </div>
      </div>
    </header>
  );
};
