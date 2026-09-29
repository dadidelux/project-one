import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';
import { BookOpen, Award, TrendingUp } from 'lucide-react';

export default function MyLearningPage() {
  const [enrollments, setEnrollments] = useState([]);
  const [certificates, setCertificates] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.get('/enrollments/').catch(() => ({ data: [] })),
      api.get('/certificates/').catch(() => ({ data: [] })),
    ]).then(([enrollRes, certRes]) => {
      setEnrollments(enrollRes.data.results || enrollRes.data);
      setCertificates(certRes.data.results || certRes.data);
    }).finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">My Learning</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3">
            <BookOpen className="h-8 w-8 text-primary-600" />
            <div>
              <p className="text-2xl font-bold text-gray-900">{enrollments.length}</p>
              <p className="text-sm text-gray-500">Enrolled Courses</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3">
            <Award className="h-8 w-8 text-yellow-500" />
            <div>
              <p className="text-2xl font-bold text-gray-900">{certificates.length}</p>
              <p className="text-sm text-gray-500">Certificates</p>
            </div>
          </div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="flex items-center gap-3">
            <TrendingUp className="h-8 w-8 text-green-600" />
            <div>
              <p className="text-2xl font-bold text-gray-900">
                {enrollments.length > 0 ? Math.round((certificates.length / enrollments.length) * 100) : 0}%
              </p>
              <p className="text-sm text-gray-500">Completion Rate</p>
            </div>
          </div>
        </div>
      </div>

      <h2 className="text-2xl font-bold text-gray-900 mb-4">Enrolled Courses</h2>
      {enrollments.length === 0 ? (
        <div className="text-center py-12 bg-white rounded-lg shadow">
          <BookOpen className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-4 text-lg font-medium text-gray-900">No courses yet</h3>
          <p className="mt-2 text-gray-500">Browse courses and enroll to get started.</p>
          <Link to="/courses" className="mt-4 inline-block px-6 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700">
            Browse Courses
          </Link>
        </div>
      ) : (
        <div className="space-y-4">
          {enrollments.map(enrollment => (
            <Link
              key={enrollment.id}
              to={`/courses/${enrollment.course}`}
              className="block bg-white rounded-lg shadow p-6 hover:shadow-md transition-shadow"
            >
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">{enrollment.course_title}</h3>
                  <p className="text-sm text-gray-500">
                    Enrolled {new Date(enrollment.enrolled_at).toLocaleDateString()}
                    {enrollment.enrollment_type === 'self' ? ' · Self-enrolled' : ' · Admin-enrolled'}
                  </p>
                </div>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                  enrollment.is_active ? 'bg-green-100 text-green-700' : 'bg-gray-100 text-gray-500'
                }`}>
                  {enrollment.is_active ? 'Active' : 'Inactive'}
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}

      {certificates.length > 0 && (
        <>
          <h2 className="text-2xl font-bold text-gray-900 mb-4 mt-12">Certificates</h2>
          <div className="space-y-4">
            {certificates.map(cert => (
              <div key={cert.id} className="bg-white rounded-lg shadow p-6 border-l-4 border-yellow-400">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">{cert.course_title}</h3>
                    <p className="text-sm text-gray-500">
                      Certificate ID: {cert.certificate_id} · Issued {new Date(cert.issued_at).toLocaleDateString()}
                    </p>
                  </div>
                  <Award className="h-8 w-8 text-yellow-500" />
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
