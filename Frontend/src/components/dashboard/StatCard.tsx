import React from 'react';

export interface StatCardProps {
  label: string;
  value: number | string;
  icon: React.ReactNode;
  theme: 'blue' | 'purple' | 'emerald' | 'green' | 'amber';
}

export const StatCard: React.FC<StatCardProps> = ({ label, value, icon, theme }) => {
  return (
    <div className="stat-card">
      <div className={`stat-icon-wrapper ${theme}`}>
        {icon}
      </div>
      <div className="stat-info">
        <span className="stat-value">{value}</span>
        <span className="stat-label">{label}</span>
      </div>
    </div>
  );
};
