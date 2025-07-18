// Smart Event Matcher Event Card Styles - Warm Color Palette
export const eventCardStyles = {
  card: {
    background: 'linear-gradient(135deg, #ffffff 0%, #FFD6E8 100%)',
    border: '1px solid #f0f0f0',
    borderRadius: '12px',
    padding: '1.8rem',
    boxShadow: '0 3px 15px rgba(0, 0, 0, 0.08)',
    transition: 'all 0.3s ease',
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
    maxWidth: '400px',
    width: '100%',
    position: 'relative',
    overflow: 'hidden',
    fontFamily: "'Poppins', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
  },
  
  cardHover: {
    boxShadow: '0 12px 32px rgba(0, 0, 0, 0.15)',
    transform: 'translateY(-6px) scale(1.02)',
    borderColor: '#F9A826',
  },
  
  cardBorder: {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: '4px',
    background: 'linear-gradient(90deg, #F9A826 0%, #C1A1D3 100%)',
  },
  
  title: {
    color: '#2c2c2c',
    fontSize: '1.4rem',
    fontWeight: '600',
    margin: '0 0 0.8rem 0',
    lineHeight: '1.3',
  },
  
  description: {
    color: '#666',
    fontSize: '0.95rem',
    marginBottom: '1rem',
    lineHeight: '1.5',
  },
  
  details: {
    display: 'flex',
    gap: '1.2rem',
    marginBottom: '1rem',
    fontSize: '0.85rem',
    color: '#666',
    flexWrap: 'wrap',
  },
  
  detailItem: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.4rem',
  },
  
  keywords: {
    color: '#C1A1D3',
    fontSize: '0.85rem',
    marginBottom: '1rem',
    fontWeight: '500',
  },
  
  matchScore: {
    background: 'linear-gradient(135deg, #F9A826 0%, #FFD6E8 100%)',
    color: '#ffffff',
    padding: '0.4rem 0.8rem',
    borderRadius: '20px',
    fontSize: '0.8rem',
    fontWeight: '600',
    position: 'absolute',
    top: '1rem',
    right: '1rem',
    animation: 'pulse 2s ease-in-out infinite',
  },
  
  platformIcon: {
    width: '24px',
    height: '24px',
    borderRadius: '50%',
    background: '#C1A1D3',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    color: '#ffffff',
    fontSize: '0.7rem',
    fontWeight: '600',
  },
  
  actions: {
    marginTop: '1.5rem',
    display: 'flex',
    gap: '0.75rem',
  },
  
  button: {
    background: '#F9A826',
    color: '#ffffff',
    border: '1px solid #F9A826',
    borderRadius: '8px',
    padding: '0.75rem 1.5rem',
    fontSize: '0.9rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    textDecoration: 'none',
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
  },
  
  buttonHover: {
    background: '#e6971f',
    borderColor: '#e6971f',
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 20px rgba(249, 168, 38, 0.3)',
  },
  
  buttonSecondary: {
    background: '#ffffff',
    color: '#C1A1D3',
    border: '1px solid #C1A1D3',
  },
  
  buttonSecondaryHover: {
    background: '#C1A1D3',
    color: '#ffffff',
    boxShadow: '0 4px 16px rgba(193, 161, 211, 0.2)',
  },
  
  matchBadge: {
    background: 'linear-gradient(135deg, #F9A826 0%, #C1A1D3 100%)',
    color: '#ffffff',
    padding: '0.35rem 0.75rem',
    borderRadius: '20px',
    fontSize: '0.8rem',
    fontWeight: '600',
  },
  
  tag: {
    background: '#FFD6E8',
    color: '#2c2c2c',
    padding: '0.25rem 0.75rem',
    borderRadius: '20px',
    fontSize: '0.8rem',
    fontWeight: '500',
    border: '1px solid #f0f0f0',
    transition: 'all 0.3s ease',
    display: 'inline-block',
    margin: '0.25rem 0.5rem 0.25rem 0',
  },
  
  tagHover: {
    background: '#C1A1D3',
    color: '#ffffff',
    transform: 'translateY(-2px)',
  },
};
