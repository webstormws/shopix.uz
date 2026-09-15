import { useState, useEffect } from 'react';
import { dashboardAPI } from '../services/api';
import Header from '../components/Header';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    dashboardAPI.stats().then((res) => {
      setStats(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Yuklanmoqda...</div>;
  if (!stats) return <div className="error">Ma'lumot olishda xatolik</div>;

  const statCards = [
    { label: 'Foydalanuvchilar', value: stats.total_users, color: '#6366f1', icon: '👥' },
    { label: 'Mahsulotlar', value: stats.total_products, color: '#10b981', icon: '📦' },
    { label: 'Buyurtmalar', value: stats.total_orders, color: '#f59e0b', icon: '🛒' },
    { label: 'Umumiy daromad', value: `${(stats.total_revenue).toLocaleString()} so'm`, color: '#ef4444', icon: '💰' },
    { label: 'Bugungi tashriflar', value: stats.visits_today, color: '#8b5cf6', icon: '👁️' },
    { label: '30 kunlik tashriflar', value: stats.visits_last_30_days, color: '#06b6d4', icon: '📈' },
  ];

  const statusLabels = {
    new: 'Qabul qilindi',
    preparing: 'Tayyorlanmoqda',
    on_the_way: "Yo'lda",
    delivered: 'Yetkazib berildi',
    cancelled: 'Bekor qilindi',
  };

  const maxOrders = Math.max(...stats.daily_stats.map((d) => d.orders), 1);

  return (
    <>
      <Header title="Dashboard" />
      <div className="content">
        <div className="stats-grid">
          {statCards.map((card) => (
            <div key={card.label} className="stat-card">
              <div className="stat-icon" style={{ background: card.color + '20', color: card.color }}>
                {card.icon}
              </div>
              <div className="stat-info">
                <span className="stat-value">{card.value}</span>
                <span className="stat-label">{card.label}</span>
              </div>
            </div>
          ))}
        </div>

        <div className="dashboard-grid">
          <div className="card">
            <h3>Buyurtmalar (14 kun)</h3>
            <div className="chart">
              {stats.daily_stats.map((day) => (
                <div key={day.date} className="chart-bar-wrapper">
                  <div className="chart-bar" style={{ height: `${(day.orders / maxOrders) * 100}%` }}>
                    <span className="chart-tooltip">{day.orders}</span>
                  </div>
                  <span className="chart-label">{day.date.slice(5)}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="card">
            <h3>Status bo'yicha</h3>
            <div className="status-list">
              {stats.orders_by_status.map((item) => (
                <div key={item.status} className="status-item">
                  <span className="status-dot" data-status={item.status}></span>
                  <span>{statusLabels[item.status] || item.status}</span>
                  <span className="status-count">{item.count}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="card">
          <h3>So'nggi buyurtmalar</h3>
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Foydalanuvchi</th>
                  <th>Status</th>
                  <th>Summa</th>
                  <th>Sana</th>
                </tr>
              </thead>
              <tbody>
                {stats.recent_orders.map((order) => (
                  <tr key={order.id}>
                    <td>#{order.id}</td>
                    <td>{order.user__username}</td>
                    <td>
                      <span className={`badge badge-${order.status}`}>
                        {statusLabels[order.status] || order.status}
                      </span>
                    </td>
                    <td>{Number(order.total).toLocaleString()} so'm</td>
                    <td>{new Date(order.created_at).toLocaleDateString('uz-UZ')}</td>
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
