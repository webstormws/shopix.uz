import { useState, useEffect } from 'react';
import { reviewsAPI } from '../services/api';
import Header from '../components/Header';

export default function Reviews() {
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    reviewsAPI.list().then((res) => {
      setReviews(res.data.results || res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">Yuklanmoqda...</div>;

  return (
    <>
      <Header title="Sharhlar" />
      <div className="content">
        <div className="card">
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Foydalanuvchi</th>
                  <th>Mahsulot ID</th>
                  <th>Reyting</th>
                  <th>Sharh</th>
                  <th>Sana</th>
                </tr>
              </thead>
              <tbody>
                {reviews.length === 0 && (
                  <tr><td colSpan={6} className="empty-state">Sharhlar topilmadi</td></tr>
                )}
                {reviews.map((r) => (
                  <tr key={r.id}>
                    <td>{r.id}</td>
                    <td>{r.username}</td>
                    <td>#{r.product}</td>
                    <td>
                      <div className="stars">
                        {[1, 2, 3, 4, 5].map((s) => (
                          <span key={s} className={s <= r.rating ? 'star filled' : 'star'}>★</span>
                        ))}
                      </div>
                    </td>
                    <td className="review-text">{r.comment || '—'}</td>
                    <td>{new Date(r.created_at).toLocaleDateString('uz-UZ')}</td>
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
