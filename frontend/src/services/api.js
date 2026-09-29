import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (credentials) => api.post('/users/login/', credentials),
  register: (userData) => api.post('/users/register/', userData),
  getProfile: () => api.get('/users/me/'),
};

export const coursesAPI = {
  list: () => api.get('/courses/'),
  get: (id) => api.get(`/courses/${id}/`),
  enroll: (courseId) => api.post('/enrollments/self_enroll/', { course_id: courseId }),
};

export const certificatesAPI = {
  list: () => api.get('/certificates/'),
  issue: (courseId) => api.post('/certificates/issue/', { course_id: courseId }),
};

export const progressAPI = {
  list: () => api.get('/progress/'),
  complete: (progressId) => api.post(`/progress/${progressId}/complete/`),
  getCourseProgress: (courseId) => api.get(`/progress/course-progress/?course_id=${courseId}`),
  create: (lessonId) => api.post('/progress/', { lesson: lessonId }),
};

export default api;