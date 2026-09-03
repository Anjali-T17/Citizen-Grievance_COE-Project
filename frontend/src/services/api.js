import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const authAPI = {
  demoLogin: (organisation, role) => api.post('/auth/demo-login', { organisation, role }),
};

export const orgAPI = {
  getOrganisations: () => api.get('/organisations'),
  getRoles: (org_id) => api.get('/roles', { params: { org_id } }),
};

export const complaintAPI = {
  createComplaint: (data, userId = 'USER_001') =>
    api.post('/complaints', data, { params: { user_id: userId } }),
  getComplaints: () => api.get('/complaints'),
  getComplaintById: (id) => api.get(`/complaints/${id}`),
  uploadAttachment: (id, formData) =>
    api.post(`/complaints/${id}/attachments`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
};

export const featureAPI = {
  getFeatures: (role, org) => api.get('/features', { params: { role, org } }),
  getFeatureById: (id, role, org) => api.get(`/features/${id}`, { params: { role, org } }),
};

export const recommendationAPI = {
  getRecommendation: (payload) => api.post('/recommendations', payload),
};

export const overrideAPI = {
  recordOverride: (payload) => api.post('/overrides', payload),
};

export const analyticsAPI = {
  getUsageAnalytics: () => api.get('/analytics/usage'),
};

export default api;
