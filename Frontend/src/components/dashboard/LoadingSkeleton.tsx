import React from 'react';

export const LoadingSkeleton: React.FC = () => {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
      {/* 5 Stats Skeletons */}
      <div className="stats-grid">
        {[1, 2, 3, 4, 5].map((i) => (
          <div key={i} className="stat-card" style={{ gap: '1rem' }}>
            <div className="skeleton" style={{ width: '44px', height: '44px', borderRadius: '10px' }} />
            <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', flex: 1 }}>
              <div className="skeleton" style={{ width: '40px', height: '24px' }} />
              <div className="skeleton" style={{ width: '80px', height: '14px' }} />
            </div>
          </div>
        ))}
      </div>

      {/* Two columns skeletons */}
      <div className="dashboard-content-split">
        <div className="content-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <div className="skeleton" style={{ width: '220px', height: '22px' }} />
            <div className="skeleton" style={{ width: '60px', height: '18px' }} />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="skeleton" style={{ width: '100%', height: '54px', borderRadius: '8px' }} />
            ))}
          </div>
        </div>

        <div className="content-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1.5rem' }}>
            <div className="skeleton" style={{ width: '140px', height: '22px' }} />
            <div className="skeleton" style={{ width: '60px', height: '18px' }} />
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="skeleton" style={{ width: '100%', height: '50px', borderRadius: '8px' }} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
