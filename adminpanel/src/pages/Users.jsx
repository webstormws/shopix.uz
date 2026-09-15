import { useState, useEffect } from 'react';
import { usersAPI } from '../services/api';
import Header from '../components/Header';

export default function Users() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    usersAPI.list().then((res) => {
      setUsers(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Yuklanmoqda...</div>;

  return (
    <>
      <Header title="Foydalanuvchilar" />
      <div className="content">
        <div className="card">
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Foydalanuvchi</th>
                  <th>Telefon</th>
                  <th>Email</th>
                  <th>Sotuvchi</th>
                  <th>Admin</th>
                  <th>Qo'shilgan</th>
                </tr>
              </thead>
              <tbody>
                {users.length === 0 && (
                  <tr><td colSpan={7} className="empty-state">Foydalanuvchilar topilmadi</td></tr>
                )}
                {users.map((u) => (
                  <tr key={u.id}>
                    <td>{u.id}</td>
                    <td>
                      <div className="user-cell">
                        <div className="user-avatar-sm">{u.username?.[0]?.toUpperCase()}</div>
                        {u.username}
                      </div>
                    </td>
                    <td>{u.phone || '—'}</td>
                    <td>{u.email || '—'}</td>
                    <td>
                      <span className={`badge ${u.is_seller ? 'badge-active' : 'badge-inactive'}`}>
                        {u.is_seller ? 'Ha' : 'Yo\'q'}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${u.is_staff ? 'badge-active' : 'badge-inactive'}`}>
                        {u.is_staff ? 'Ha' : 'Yo\'q'}
                      </span>
                    </td>
                    <td>{new Date(u.date_joined).toLocaleDateString('uz-UZ')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </>
  );
}