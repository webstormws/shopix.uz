import axios from 'axios';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
});

const formConfig = {
  headers: { 'Content-Type': undefined },
};

api.interceptors.request.use((config) => {
  const access = localStorage.getItem('access');
  if (access) {
    config.headers.Authorization = `Bearer ${access}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const original = err.config;
    if (err.response?.status === 401 && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem('refresh');
      if (refresh) {
        try {
          const res = await axios.post(`${API_BASE}/accounts/login/refresh/`, { refresh });
          localStorage.setItem('access', res.data.access);
          if (res.data.refresh) localStorage.setItem('refresh', res.data.refresh);
          original.headers.Authorization = `Bearer ${res.data.access}`;
          return api(original);
        } catch {
          localStorage.removeItem('access');
          localStorage.removeItem('refresh');
          localStorage.removeItem('user');
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(err);
  }
);

export const authAPI = {
  login: (data) => api.post('/accounts/login/', data),
  register: (data) => api.post('/accounts/register/', data),
  profile: () => api.get('/accounts/profile/'),
};

export const dashboardAPI = {
  stats: () => api.get('/analytics/dashboard/'),
};

export const categoriesAPI = {
  list: () => api.get('/catalog/categories/'),
  create: (data) => api.post('/catalog/categories/', data, formConfig),
  update: (id, data) => api.put(`/catalog/categories/${id}/`, data, formConfig),
  delete: (id) => api.delete(`/catalog/categories/${id}/`),
};

export const marketsAPI = {
  list: () => api.get('/catalog/markets/'),
  create: (data) => api.post('/catalog/markets/', data, formConfig),
  update: (id, data) => api.put(`/catalog/markets/${id}/`, data, formConfig),
  delete: (id) => api.delete(`/catalog/markets/${id}/`),
};

export const productsAPI = {
  list: (params) => api.get('/catalog/products/', { params }),
  get: (id) => api.get(`/catalog/products/${id}/`),
  create: (data) => api.post('/catalog/products/', data, formConfig),
  update: (id, data) => api.put(`/catalog/products/${id}/`, data, formConfig),
  delete: (id) => api.delete(`/catalog/products/${id}/`),
};

export const ordersAPI = {
  list: () => api.get('/orders/orders/'),
  get: (id) => api.get(`/orders/orders/${id}/`),
  updateStatus: (id, status) => api.patch(`/orders/orders/${id}/status/`, { status }),
};

export const usersAPI = {
  list: () => api.get('/accounts/users/'),
};

export const reviewsAPI = {
  list: (params) => api.get('/catalog/reviews/', { params }),
};

export default api;
