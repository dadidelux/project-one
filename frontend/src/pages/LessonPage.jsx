import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import api, { progressAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import { toast } from 'react-hot-toast';
import { ChevronLeft, ChevronRight, CheckCircle } from 'lucide-react';
import LessonContentAccordion from '../components/LessonContentAccordion';

export default function LessonPage() {
  const { courseId, chapterId, lessonId } = useParams();
  const { user } = useAuth();
  const navigate = useNavigate();
  const [lesson, setLesson] = useState(null);
  const [chapter, setChapter] = useState(null);
  const [completed, setCompleted] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get(`/courses/${courseId}/chapters/${chapterId}/lessons/${lessonId}/`)
      .then(res => setLesson(res.data))
      .catch(() => toast.error('Failed to load lesson'))
      .finally(() => setLoading(false));

    api.get(`/courses/${courseId}/chapters/${chapterId}/`)
      .then(res => setChapter(res.data))
      .catch(() => {});
  }, [courseId, chapterId, lessonId]);

  useEffect(() => {
    if (lesson && user) {
      progressAPI.list()
        .then(res => {
          const progresses = res.data.results || res.data;
          const p = progresses.find(pr => pr.lesson == lesson.id);
          if (p) setCompleted(p.completed);
        })
        .catch(() => {});
    }
  }, [lesson, user]);

  const handleComplete = async () => {
    try {
      let progress;
      const list = await progressAPI.list();
      const progresses = list.data.results || list.data;
      const existing = progresses.find(p => p.lesson == lesson.id);

      if (existing) {
        await progressAPI.complete(existing.id);
      } else {
        const created = await progressAPI.create(lesson.id);
        await progressAPI.complete(created.data.id);
      }
      setCompleted(true);
      toast.success('Lesson completed!');
    } catch (err) {
      toast.error('Failed to mark as complete');
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-4xl mx-auto px-4 py-16 text-center">
        <h2 className="text-2xl font-bold text-gray-900">Lesson not found</h2>
      </div>
    );
  }

  const lessons = chapter?.lessons || [];
  const currentIndex = lessons.findIndex(l => l.id == lesson.id);
  const prevLesson = currentIndex > 0 ? lessons[currentIndex - 1] : null;
  const nextLesson = currentIndex < lessons.length - 1 ? lessons[currentIndex + 1] : null;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
      <div className="mb-4">
        <button
          onClick={() => navigate(`/courses/${courseId}`)}
          className="text-primary-600 hover:text-primary-500 text-sm font-medium flex items-center gap-1"
        >
          <ChevronLeft size={16} /> Back to course
        </button>
      </div>

      <div className="bg-white rounded-lg shadow overflow-hidden">
        <div className="px-8 py-6 border-b bg-gray-50">
          <p className="text-sm text-gray-500">Chapter {chapterId} · Lesson {currentIndex + 1} of {lessons.length}</p>
          <h1 className="text-2xl font-bold text-gray-900 mt-1">{lesson.title}</h1>
        </div>

        <div className="px-8 py-8">
          {lesson.content ? (
            <LessonContentAccordion content={lesson.content} />
          ) : (
            <p className="text-gray-500 italic">No content for this lesson yet.</p>
          )}
        </div>

        <div className="px-8 py-6 border-t bg-gray-50 flex items-center justify-between">
          <div>
            {completed ? (
              <span className="inline-flex items-center gap-2 text-green-600 font-medium">
                <CheckCircle size={20} /> Completed
              </span>
            ) : (
              <button
                onClick={handleComplete}
                className="px-5 py-2 bg-green-600 text-white font-medium rounded-lg hover:bg-green-700 transition-colors"
              >
                Mark as Complete
              </button>
            )}
          </div>

          <div className="flex items-center gap-3">
            {prevLesson ? (
              <button
                onClick={() => navigate(`/courses/${courseId}/chapters/${chapterId}/lessons/${prevLesson.id}`)}
                className="flex items-center gap-1 px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                <ChevronLeft size={16} /> Previous
              </button>
            ) : null}
            {nextLesson ? (
              <button
                onClick={() => navigate(`/courses/${courseId}/chapters/${chapterId}/lessons/${nextLesson.id}`)}
                className="flex items-center gap-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Next <ChevronRight size={16} />
              </button>
            ) : (
              <button
                onClick={() => navigate(`/courses/${courseId}`)}
                className="flex items-center gap-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Back to Course
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
