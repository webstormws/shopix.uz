import { NavLink, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import LOGO from '../assets/LOGO.png';

const menuItems = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/products', label: 'Mahsulotlar', icon: '📦' },
  { path: '/categories', label: 'Kategoriyalar', icon: '🏷️' },
  { path: '/markets', label: "Do'konlar", icon: '🏪' },
  { path: '/orders', label: 'Buyurtmalar', icon: '🛒' },
  { path: '/users', label: 'Foydalanuvchilar', icon: '👥' },
  { path: '/reviews', label: 'Sharhlar', icon: '⭐' },
];

export default function Sidebar() {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-logo">
        <img src={LOGO} alt="Shopix Admin" className="logo-img" />
        <span className="logo-text">Shopix Admin</span>
      </div>
      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            end={item.path === '/'}
            className={({ isActive }) => `sidebar-link ${isActive ? 'active' : ''}`}
          >
            <span className="sidebar-icon">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
      <button className="sidebar-logout" onClick={handleLogout}>
        <span>🚪</span>
        <span>Chiqish</span>
      </button>
    </aside>
  );
}
