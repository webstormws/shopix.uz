import { useState, useEffect } from 'react';
import { marketsAPI } from '../services/api';
import Header from '../components/Header';

const resolveImage = (url) => {
  if (!url) return null;
  if (url.startsWith('http')) return url;
  return `https://hearty-learning-production-d991.up.railway.app${url}`;
};

export default function Markets() {
  const [markets, setMarkets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ name: '', address: '', rating: '5.0', open_time: '09:00', close_time: '23:00', is_open: true });
  const [logoFile, setLogoFile] = useState(null);
  const [logoName, setLogoName] = useState('');

  const load = () => {
    marketsAPI.list().then((res) => {
      setMarkets(res.data.results || res.data);
      setLoading(false);
    });
  };

  useEffect(() => { load(); }, []);

  const openCreate = () => {
    setEditing(null);
    setForm({ name: '', address: '', rating: '5.0', open_time: '09:00', close_time: '23:00', is_open: true });
    setLogoFile(null);
    setLogoName('');
    setShowModal(true);
  };

  const openEdit = (m) => {
    setEditing(m);
    setForm({
      name: m.name, address: m.address || '', rating: String(m.rating),
      open_time: m.open_time || '09:00', close_time: m.close_time || '23:00', is_open: m.is_open,
    });
    setLogoFile(null);
    setLogoName('');
    setShowModal(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append('name', form.name);
    data.append('address', form.address || '');
    data.append('rating', Number(form.rating));
    data.append('open_time', form.open_time);
    data.append('close_time', form.close_time);
    data.append('is_open', form.is_open);
    if (logoFile) data.append('logo', logoFile);

    if (editing) {
      await marketsAPI.update(editing.id, data);
    } else {
      await marketsAPI.create(data);
    }
    setShowModal(false);
    load();
  };

  const handleDelete = async (id) => {
    if (confirm("O'chirmoqchimisiz?")) {
      await marketsAPI.delete(id);
      load();
    }
  };

  if (loading) return <div className="loading">Yuklanmoqda...</div>;

  return (
    <>
      <Header title="Do'konlar" />
      <div className="content">
        <div className="toolbar">
          <button className="btn btn-primary" onClick={openCreate}>+ Yangi do'kon</button>
        </div>
        <div className="card">
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Rasm</th>
                  <th>Nomi</th>
                  <th>Manzil</th>
                  <th>Reyting</th>
                  <th>Ish vaqti</th>
                  <th>Holat</th>
                  <th>Amallar</th>
                </tr>
              </thead>
              <tbody>
                {markets.map((m) => (
                  <tr key={m.id}>
                    <td>{m.id}</td>
                    <td>
                      {m.logo ? (
                        <img
                          src={resolveImage(m.logo)}
                          alt={m.name}
                          className="table-img"
                          onError={(e) => { e.target.style.visibility = 'hidden'; }}
                        />
                      ) : (
                        <span className="no-img">Rasm yo'q</span>
                      )}
                    </td>
                    <td>{m.name}</td>
                    <td>{m.address || '—'}</td>
                    <td>⭐ {m.rating}</td>
                    <td>{m.open_time} - {m.close_time}</td>
                    <td>
                      <span className={`badge ${m.is_open ? 'badge-active' : 'badge-inactive'}`}>
                        {m.is_open ? 'Ochiq' : 'Yopiq'}
                      </span>
                    </td>
                    <td>
                      <div className="actions">
                        <button className="btn btn-sm btn-edit" onClick={() => openEdit(m)}>Tahrirlash</button>
                        <button className="btn btn-sm btn-delete" onClick={() => handleDelete(m.id)}>O'chirish</button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {showModal && (
          <div className="modal-overlay" onClick={() => setShowModal(false)}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
              <h3>{editing ? "Do'koni tahrirlash" : "Yangi do'kon"}</h3>
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Logotip</label>
                  <input type="file" accept="image/*" onChange={(e) => {
                    const f = e.target.files?.[0];
                    setLogoFile(f || null);
                    setLogoName(f ? f.name : '');
                  }} />
                  {logoName && <span className="file-name">{logoName}</span>}
                </div>
                <div className="form-group">
                  <label>Nomi</label>
                  <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
                </div>
                <div className="form-group">
                  <label>Manzil</label>
                  <input value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Reyting</label>
                    <input type="number" step="0.1" min="0" max="5" value={form.rating} onChange={(e) => setForm({ ...form, rating: e.target.value })} />
                  </div>
                  <div className="form-group">
                    <label>Ochilish</label>
                    <input type="time" value={form.open_time} onChange={(e) => setForm({ ...form, open_time: e.target.value })} />
                  </div>
                  <div className="form-group">
                    <label>Yopilish</label>
                    <input type="time" value={form.close_time} onChange={(e) => setForm({ ...form, close_time: e.target.value })} />
                  </div>
                </div>
                <div className="form-group">
                  <label className="checkbox-label">
                    <input type="checkbox" checked={form.is_open} onChange={(e) => setForm({ ...form, is_open: e.target.checked })} />
                    Ochiq
                  </label>
                </div>
                <div className="modal-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Bekor qilish</button>
                  <button type="submit" className="btn btn-primary">{editing ? 'Saqlash' : 'Yaratish'}</button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
