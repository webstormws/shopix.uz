import { useState, useEffect } from 'react';
import { productsAPI, categoriesAPI, marketsAPI } from '../services/api';
import Header from '../components/Header';

const resolveImage = (url) => {
  if (!url) return null;
  if (url.startsWith('http')) return url;
  return `http://127.0.0.1:8000${url}`;
};

export default function Products() {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [markets, setMarkets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [form, setForm] = useState({ name: '', price: '', unit: 'dona', stock: '', category: '', market: '', description: '', is_active: true });
  const [imageFile, setImageFile] = useState(null);
  const [imageName, setImageName] = useState('');
  const [error, setError] = useState('');
  const [saving, setSaving] = useState(false);

  const load = () => {
    Promise.all([productsAPI.list(), categoriesAPI.list(), marketsAPI.list()])
      .then(([p, c, m]) => {
        setProducts(p.data.results || p.data);
        setCategories(c.data.results || c.data);
        setMarkets(m.data.results || m.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  };

  useEffect(() => { load(); }, []);

  const openCreate = () => {
    setEditing(null);
    setForm({ name: '', price: '', unit: 'dona', stock: '', category: '', market: '', description: '', is_active: true });
    setImageFile(null);
    setImageName('');
    setError('');
    setShowModal(true);
  };

  const openEdit = (p) => {
    setEditing(p);
    setForm({
      name: p.name, price: p.price, unit: p.unit, stock: p.stock,
      category: p.category || '', market: p.market || '',
      description: p.description || '', is_active: p.is_active,
    });
    setImageFile(null);
    setImageName('');
    setError('');
    setShowModal(true);
  };

  const formatErrors = (err) => {
    const d = err.response?.data;
    if (!d) return 'Server xatolik. Iltimos, qayta urinib ko\'ring.';
    if (typeof d === 'object') {
      return Object.entries(d)
        .map(([key, msgs]) => {
          const label = {
            name: 'Nomi', price: 'Narxi', unit: 'Birlik', stock: 'Zaxira',
            market: "Do'kon", category: 'Kategoriya', image: 'Rasm',
            description: 'Tavsif', old_price: 'Eski narx', is_active: 'Holat',
          }[key] || key;
          const msg = Array.isArray(msgs) ? msgs.join(', ') : String(msgs);
          return `${label}: ${msg}`;
        })
        .join('; ');
    }
    return String(d.detail || d);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    if (!form.market) {
      setError("Do'kon tanlash shart");
      return;
    }
    const data = new FormData();
    data.append('name', form.name);
    data.append('price', Number(form.price));
    data.append('unit', form.unit);
    data.append('stock', Number(form.stock));
    if (form.category) data.append('category', form.category);
    data.append('market', form.market);
    data.append('description', form.description || '');
    data.append('is_active', form.is_active);
    if (imageFile) data.append('image', imageFile);

    setSaving(true);
    try {
      if (editing) {
        await productsAPI.update(editing.id, data);
      } else {
        await productsAPI.create(data);
      }
      setShowModal(false);
      load();
    } catch (err) {
      setError(formatErrors(err));
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id) => {
    if (confirm('O\'chirmoqchimisiz?')) {
      await productsAPI.delete(id);
      load();
    }
  };

  if (loading) return <div className="loading">Yuklanmoqda...</div>;

  return (
    <>
      <Header title="Mahsulotlar" />
      <div className="content">
        <div className="toolbar">
          <button className="btn btn-primary" onClick={openCreate}>+ Yangi mahsulot</button>
        </div>
        <div className="card">
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Rasm</th>
                  <th>Nomi</th>
                  <th>Narxi</th>
                  <th>Birlik</th>
                  <th>Zaxira</th>
                  <th>Do'kon</th>
                  <th>Holat</th>
                  <th>Amallar</th>
                </tr>
              </thead>
              <tbody>
                {products.map((p) => (
                  <tr key={p.id}>
                    <td>{p.id}</td>
                    <td>
                      {p.image ? (
                        <img
                          src={resolveImage(p.image)}
                          alt={p.name}
                          className="table-img"
                          onError={(e) => { e.target.style.visibility = 'hidden'; }}
                        />
                      ) : (
                        <span className="no-img">Rasm yo'q</span>
                      )}
                    </td>
                    <td>{p.name}</td>
                    <td>{Number(p.price).toLocaleString()} so'm</td>
                    <td>{p.unit}</td>
                    <td>{p.stock}</td>
                    <td>{p.market_name}</td>
                    <td>
                      <span className={`badge ${p.is_active ? 'badge-active' : 'badge-inactive'}`}>
                        {p.is_active ? 'Faol' : 'Nofaol'}
                      </span>
                    </td>
                    <td>
                      <div className="actions">
                        <button className="btn btn-sm btn-edit" onClick={() => openEdit(p)}>Tahrirlash</button>
                        <button className="btn btn-sm btn-delete" onClick={() => handleDelete(p.id)}>O'chirish</button>
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
              <h3>{editing ? 'Mahsulotni tahrirlash' : 'Yangi mahsulot'}</h3>
              {error && <div className="login-error">{error}</div>}
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Nomi</label>
                  <input value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
                </div>
                <div className="form-group">
                  <label>Rasm</label>
                  <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => {
                      const file = e.target.files?.[0];
                      setImageFile(file || null);
                      setImageName(file ? file.name : '');
                    }}
                  />
                  {imageName && <span className="file-name">{imageName}</span>}
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Narxi (so'm)</label>
                    <input type="number" value={form.price} onChange={(e) => setForm({ ...form, price: e.target.value })} required />
                  </div>
                  <div className="form-group">
                    <label>Birlik</label>
                    <select value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })}>
                      <option value="dona">dona</option>
                      <option value="kg">kg</option>
                      <option value="litr">litr</option>
                      <option value="pachka">pachka</option>
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Zaxira</label>
                    <input type="number" value={form.stock} onChange={(e) => setForm({ ...form, stock: e.target.value })} required />
                  </div>
                </div>
                <div className="form-row">
                  <div className="form-group">
                    <label>Kategoriya</label>
                    <select value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })}>
                      <option value="">Tanlang</option>
                      {categories.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                    </select>
                  </div>
                  <div className="form-group">
                    <label>Do'kon <span className="req">*</span></label>
                    <select value={form.market} onChange={(e) => setForm({ ...form, market: e.target.value })} required>
                      <option value="">Tanlang</option>
                      {markets.map((m) => <option key={m.id} value={m.id}>{m.name}</option>)}
                    </select>
                  </div>
                </div>
                <div className="form-group">
                  <label>Tavsif</label>
                  <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} rows={3} />
                </div>
                <div className="form-group">
                  <label className="checkbox-label">
                    <input type="checkbox" checked={form.is_active} onChange={(e) => setForm({ ...form, is_active: e.target.checked })} />
                    Faol
                  </label>
                </div>
                <div className="modal-actions">
                  <button type="button" className="btn btn-secondary" onClick={() => setShowModal(false)}>Bekor qilish</button>
                  <button type="submit" className="btn btn-primary" disabled={saving}>
                    {saving ? 'Saqlanmoqda...' : (editing ? 'Saqlash' : 'Yaratish')}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </>
  );
}
