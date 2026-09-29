import { useState, useEffect } from 'react';
import { useParams, useNavigate, Link } from 'react-router-dom';
import { coursesAPI, progressAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-hot-toast';
import { ArrowLeft, CheckCircle, BookOpen } from 'lucide-react';

export default function LessonViewPage() {
  const { courseId, lessonId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [lesson, setLesson] = useState(null);
  const [loading, setLoading] = useState(true);
  const [completed, setCompleted] = useState(false);
  const [marking, setMarking] = useState(false);

  useEffect(() => {
    coursesAPI.get(courseId)
      .then(res => {
        setCourse(res.data);
        for (const chapter of res.data.chapters || []) {
          const found = chapter.lessons?.find(l => l.id === parseInt(lessonId));
          if (found) {
            setLesson(found);
            break;
          }
        }
      })
      .catch(() => toast.error('Failed to load lesson'))
      .finally(() => setLoading(false));
  }, [courseId, lessonId]);

  const handleMarkComplete = async () => {
    setMarking(true);
    try {
      let progressData;
      try {
        const res = await progressAPI.list();
        progressData = res.data.find(p => p.lesson === parseInt(lessonId));
      } catch {
        progressData = null;
      }

      if (progressData) {
        await progressAPI.complete(progressData.id);
      } else {
        const createRes = await progressAPI.create(parseInt(lessonId));
        await progressAPI.complete(createRes.data.id);
      }

      setCompleted(true);
      toast.success('Lesson marked as complete!');
    } catch (err) {
      toast.error('Failed to mark lesson as complete');
    } finally {
      setMarking(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="text-center py-12">
        <h2 className="text-2xl font-bold text-gray-900">Lesson not found</h2>
        <Link to={`/courses/${courseId}`} className="text-primary-600 hover:underline mt-4 block">
          Back to course
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="mb-6">
        <Link
          to={`/courses/${courseId}`}
          className="flex items-center gap-2 text-primary-600 hover:text-primary-800"
        >
          <ArrowLeft size={18} />
          Back to {course?.title}
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow-lg overflow-hidden">
        <div className="p-8">
          <div className="flex justify-between items-start mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">{lesson.title}</h1>
              {course && (
                <p className="mt-2 text-gray-500">{course.title}</p>
              )}
            </div>

            {user && (
              <button
                onClick={handleMarkComplete}
                disabled={completed || marking}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg ${
                  completed
                    ? 'bg-green-100 text-green-800'
                    : 'bg-primary-600 text-white hover:bg-primary-700'
                } disabled:opacity-50`}
              >
                {completed ? (
                  <>
                    <CheckCircle size={18} />
                    Completed
                  </>
                ) : marking ? (
                  'Marking...'
                ) : (
                  'Mark as Complete'
                )}
              </button>
            )}
          </div>

          <div className="prose prose-lg max-w-none">
            <div dangerouslySetInnerHTML={{ __html: lesson.content }} />
          </div>

          <div className="mt-8 pt-6 border-t flex justify-between">
            <Link
              to={`/courses/${courseId}`}
              className="text-primary-600 hover:text-primary-800"
            >
              Course Overview
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}