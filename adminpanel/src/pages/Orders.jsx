import { useState, useEffect } from 'react';
import { ordersAPI } from '../services/api';
import Header from '../components/Header';

const STATUS_CHOICES = [
  { value: 'new', label: 'Qabul qilindi' },
  { value: 'preparing', label: 'Tayyorlanmoqda' },
  { value: 'on_the_way', label: "Yo'lda" },
  { value: 'delivered', label: 'Yetkazib berildi' },
  { value: 'cancelled', label: 'Bekor qilindi' },
];

const STATUS_MAP = Object.fromEntries(STATUS_CHOICES.map((s) => [s.value, s.label]));

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedOrder, setSelectedOrder] = useState(null);

  const load = () => {
    ordersAPI.list().then((res) => {
      setOrders(res.data.results || res.data);
      setLoading(false);
    });
  };

  useEffect(() => { load(); }, []);

  const updateStatus = async (orderId, newStatus) => {
    await ordersAPI.updateStatus(orderId, newStatus);
    load();
    if (selectedOrder?.id === orderId) {
      setSelectedOrder((prev) => ({ ...prev, status: newStatus }));
    }
  };

  if (loading) return <div className="loading">Yuklanmoqda...</div>;

  return (
    <>
      <Header title="Buyurtmalar" />
      <div className="content">
        <div className="dashboard-grid">
          <div className="card" style={{ flex: selectedOrder ? 1 : 2 }}>
            <div className="table-wrapper">
              <table>
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Foydalanuvchi</th>
                    <th>Do'kon</th>
                    <th>Status</th>
                    <th>To'lov</th>
                    <th>Summa</th>
                    <th>Sana</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.map((o) => (
                    <tr
                      key={o.id}
                      className={selectedOrder?.id === o.id ? 'row-selected' : ''}
                      onClick={() => setSelectedOrder(o)}
                      style={{ cursor: 'pointer' }}
                    >
                      <td>#{o.id}</td>
                      <td>{o.user}</td>
                      <td>{o.market_name || '—'}</td>
                      <td>
                        <span className={`badge badge-${o.status}`}>
                          {STATUS_MAP[o.status] || o.status}
                        </span>
                      </td>
                      <td>{o.payment_method === 'card' ? '💳 Karta' : '💵 Naqd'}</td>
                      <td>{Number(o.total).toLocaleString()} so'm</td>
                      <td>{new Date(o.created_at).toLocaleDateString('uz-UZ')}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {selectedOrder && (
            <div className="card order-detail">
              <h3>Buyurtma #{selectedOrder.id}</h3>
              <div className="detail-row">
                <span className="detail-label">Foydalanuvchi:</span>
                <span>{selectedOrder.user}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Do'kon:</span>
                <span>{selectedOrder.market_name || '—'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Manzil:</span>
                <span>{selectedOrder.address}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">To'lov:</span>
                <span>{selectedOrder.payment_method === 'card' ? 'Karta' : 'Naqd pul'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Summa:</span>
                <span className="detail-total">{Number(selectedOrder.total).toLocaleString()} so'm</span>
              </div>

              {selectedOrder.items?.length > 0 && (
                <div className="detail-items">
                  <h4>Tarkibi</h4>
                  {selectedOrder.items.map((item) => (
                    <div key={item.id} className="detail-item">
                      <span>{item.product_name} x{item.quantity}</span>
                      <span>{Number(item.subtotal).toLocaleString()} so'm</span>
                    </div>
                  ))}
                </div>
              )}

              <div className="status-change">
                <h4>Status o'zgartirish</h4>
                <div className="status-buttons">
                  {STATUS_CHOICES.map((s) => (
                    <button
                      key={s.value}
                      className={`btn btn-sm ${selectedOrder.status === s.value ? 'btn-active-status' : 'btn-status'}`}
                      onClick={() => updateStatus(selectedOrder.id, s.value)}
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
