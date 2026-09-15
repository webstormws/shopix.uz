import { useState, useEffect } from 'react';
import { categoriesAPI } from '../services/api';
import Header from '../components/Header';

const resolveImage = (url) => {
  if (!url) return null;
  if (url.startsWith('http')) return url;
  return `http://127.0.0.1:8000${url}`;
};

export default function Categories() {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [editing, setEditing] = useState(null);
  const [name, setName] = useState('');
  const [iconFile, setIconFile] = useState(null);
  const [iconName, setIconName] = useState('');

  const load = () => {
    categoriesAPI.list().then((res) => {
      setCategories(res.data.results || res.data);
      setLoading(false);
    });
  };

  useEffect(() => { load(); }, []);

  const openCreate = () => { setEditing(null); setName(''); setIconFile(null); setIconName(''); setShowModal(true); };
  const openEdit = (c) => { setEditing(c); setName(c.name); setIconFile(null); setIconName(''); setShowModal(true); };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const data = new FormData();
    data.append('name', name);
    if (iconFile) data.append('icon', iconFile);

    if (editing) {
      await categoriesAPI.update(editing.id, data);
    } else {
      await categoriesAPI.create(data);
    }
    setShowModal(false);
    load();
  };

  const handleDelete = async (id) => {
    if (confirm("O'chirmoqchimisiz?")) {
      await categoriesAPI.delete(id);
      load();
    }
  };

  if (loading) return <div className="loading">Yuklanmoqda...</div>;

  return (
    <>
      <Header title="Kategoriyalar" />
      <div className="content">
        <div className="toolbar">
          <button className="btn btn-primary" onClick={openCreate}>+ Yangi kategoriya</button>
        </div>
        <div className="card">
          <div className="table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Rasm</th>
                  <th>Nomi</th>
                  <th>Slug</th>
                  <th>Amallar</th>
                </tr>
              </thead>
              <tbody>
                {categories.map((c) => (
                  <tr key={c.id}>
                    <td>{c.id}</td>
                    <td>
                      {c.icon ? (
                        <img
                          src={resolveImage(c.icon)}
                          alt={c.name}
                          className="table-img"
                          onError={(e) => { e.target.style.visibility = 'hidden'; }}
                        />
                      ) : (
                        <span className="no-img">Rasm yo'q</span>
                      )}
                    </td>
                    <td>{c.name}</td>
                    <td>{c.slug}</td>
                    <td>
                      <div className="actions">
                        <button className="btn btn-sm btn-edit" onClick={() => openEdit(c)}>Tahrirlash</button>
                        <button className="btn btn-sm btn-delete" onClick={() => handleDelete(c.id)}>O'chirish</button>
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
            <div className="modal modal-sm" onClick={(e) => e.stopPropagation()}>
              <h3>{editing ? 'Kategoriyani tahrirlash' : 'Yangi kategoriya'}</h3>
              <form onSubmit={handleSubmit}>
                <div className="form-group">
                  <label>Nomi</label>
                  <input value={name} onChange={(e) => setName(e.target.value)} required autoFocus />
                </div>
                <div className="form-group">
                  <label>Icon (rasm)</label>
                  <input type="file" accept="image/*" onChange={(e) => {
                    const f = e.target.files?.[0];
                    setIconFile(f || null);
                    setIconName(f ? f.name : '');
                  }} />
                  {iconName && <span className="file-name">{iconName}</span>}
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
