import { useAuth } from '../context/AuthContext';

export default function Header({ title }) {
  const { user } = useAuth();

  return (
    <header className="header">
      <h1 className="header-title">{title}</h1>
      <div className="header-user">
        <div className="header-avatar">
          {user?.username?.[0]?.toUpperCase() || 'A'}
        </div>
        <div className="header-user-info">
          <span className="header-username">{user?.username || 'Admin'}</span>
          <span className="header-role">{user?.is_staff ? 'Admin' : user?.is_seller ? 'Sotuvchi' : 'Foydalanuvchi'}</span>
        </div>
      </div>
    </header>
  );
}
