import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { coursesAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-hot-toast';
import { BookOpen, ChevronRight, CheckCircle, Lock } from 'lucide-react';

export default function CourseDetailPage() {
  const { id } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [enrolled, setEnrolled] = useState(false);
  const [loading, setLoading] = useState(true);
  const [enrolling, setEnrolling] = useState(false);

  useEffect(() => {
    coursesAPI.get(id)
      .then(res => setCourse(res.data))
      .catch(() => toast.error('Failed to load course'))
      .finally(() => setLoading(false));
  }, [id]);

  useEffect(() => {
    if (user) {
      import('../services/api').then(({ default: api }) =>
        api.get('/enrollments/')
          .then(res => {
            const enrollments = res.data.results || res.data;
            setEnrolled(enrollments.some(e => e.course == id && e.is_active));
          })
          .catch(() => {})
      );
    }
  }, [user, id]);

  const handleEnroll = async () => {
    if (!user) {
      navigate('/login');
      return;
    }
    setEnrolling(true);
    try {
      await coursesAPI.enroll(id);
      setEnrolled(true);
      toast.success('Enrolled successfully!');
    } catch (err) {
      toast.error(err.response?.data?.error || 'Enrollment failed');
    } finally {
      setEnrolling(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold text-gray-900">Course not found</h2>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="bg-white rounded-lg shadow overflow-hidden">
        {course.thumbnail ? (
          <img src={course.thumbnail} alt={course.title} className="w-full h-64 object-cover" />
        ) : (
          <div className="w-full h-64 bg-gradient-to-br from-primary-500 to-purple-600 flex items-center justify-center">
            <BookOpen className="h-20 w-20 text-white/80" />
          </div>
        )}

        <div className="p-8">
          <h1 className="text-3xl font-bold text-gray-900">{course.title}</h1>
          <p className="mt-4 text-gray-600 text-lg">{course.description}</p>

          <div className="mt-6">
            {enrolled ? (
              <span className="inline-flex items-center gap-2 text-green-600 font-medium">
                <CheckCircle size={20} /> Enrolled
              </span>
            ) : (
              <button
                onClick={handleEnroll}
                disabled={enrolling}
                className="px-6 py-3 bg-primary-600 text-white font-medium rounded-lg hover:bg-primary-700 disabled:opacity-50 transition-colors"
              >
                {enrolling ? 'Enrolling...' : user ? 'Enroll Now' : 'Login to Enroll'}
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="mt-10">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Course Content</h2>
        {course.chapters && course.chapters.length > 0 ? (
          <div className="space-y-4">
            {course.chapters.map((chapter, ci) => (
              <div key={chapter.id} className="bg-white rounded-lg shadow overflow-hidden">
                <div className="px-6 py-4 bg-gray-50 border-b">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Chapter {ci + 1}: {chapter.title}
                  </h3>
                  {chapter.description && (
                    <p className="mt-1 text-sm text-gray-500">{chapter.description}</p>
                  )}
                </div>
                <div className="divide-y">
                  {chapter.lessons && chapter.lessons.map((lesson, li) => (
                    <div
                      key={lesson.id}
                      className={`px-6 py-4 flex items-center justify-between ${
                        enrolled || lesson.is_free
                          ? 'hover:bg-gray-50 cursor-pointer'
                          : 'bg-gray-50 opacity-60'
                      }`}
                      onClick={() => {
                        if (enrolled || lesson.is_free) {
                          navigate(`/courses/${id}/chapters/${chapter.id}/lessons/${lesson.id}`);
                        } else {
                          toast.error('Enroll to access this lesson');
                        }
                      }}
                    >
                      <div className="flex items-center gap-3">
                        <span className="text-sm text-gray-400">{ci + 1}.{li + 1}</span>
                        <span className="text-gray-900">{lesson.title}</span>
                        {lesson.is_free && (
                          <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded">Free</span>
                        )}
                      </div>
                      {enrolled || lesson.is_free ? (
                        <ChevronRight size={18} className="text-gray-400" />
                      ) : (
                        <Lock size={18} className="text-gray-400" />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">No content available yet.</p>
        )}
      </div>
    </div>
  );
}
