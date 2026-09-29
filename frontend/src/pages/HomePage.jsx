import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useAuth } from '../contexts/AuthContext';
import { BookOpen, TrendingUp, Award, Users } from 'lucide-react';

const heroContainer = {
  hidden: { opacity: 0 },
  show: { opacity: 1, transition: { staggerChildren: 0.12 } },
};

const heroItem = {
  hidden: { opacity: 0, y: 16 },
  show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
};

const features = [
  {
    icon: BookOpen,
    iconBg: 'bg-primary-100',
    iconColor: 'text-primary-600',
    title: 'Structured Learning',
    body: 'Follow a carefully designed curriculum that builds your skills progressively.',
  },
  {
    icon: TrendingUp,
    iconBg: 'bg-green-100',
    iconColor: 'text-green-600',
    title: 'Track Progress',
    body: 'Monitor your learning journey with detailed progress tracking.',
  },
  {
    icon: Award,
    iconBg: 'bg-purple-100',
    iconColor: 'text-purple-600',
    title: 'Earn Certificates',
    body: 'Complete courses to earn certificates and showcase your skills.',
  },
];

export default function HomePage() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="bg-gradient-to-br from-primary-600 to-purple-700 text-white">
        <motion.div
          className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24"
          variants={heroContainer}
          initial="hidden"
          animate="show"
        >
          <motion.h1 variants={heroItem} className="text-4xl md:text-6xl font-bold mb-6">
            Master Data Science
          </motion.h1>
          <motion.p variants={heroItem} className="text-xl md:text-2xl text-primary-100 mb-8 max-w-2xl">
            Learn Python, Statistics, Machine Learning, and more with our comprehensive curriculum based on W3Schools.
          </motion.p>
          <motion.div variants={heroItem} className="flex gap-4">
            {user ? (
              <motion.div whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.98 }}>
                <Link
                  to="/courses"
                  className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition"
                >
                  Browse Courses
                </Link>
              </motion.div>
            ) : (
              <>
                <motion.div whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.98 }}>
                  <Link
                    to="/register"
                    className="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition"
                  >
                    Get Started Free
                  </Link>
                </motion.div>
                <motion.div whileHover={{ scale: 1.04 }} whileTap={{ scale: 0.98 }}>
                  <Link
                    to="/courses"
                    className="border-2 border-white text-white px-8 py-3 rounded-lg font-semibold hover:bg-white/10 transition"
                  >
                    View Courses
                  </Link>
                </motion.div>
              </>
            )}
          </motion.div>
        </motion.div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <motion.div
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
          initial="hidden"
          whileInView="show"
          viewport={{ once: true, amount: 0.3 }}
          variants={{ hidden: {}, show: { transition: { staggerChildren: 0.15 } } }}
        >
          {features.map(({ icon: Icon, iconBg, iconColor, title, body }) => (
            <motion.div
              key={title}
              variants={{
                hidden: { opacity: 0, y: 20 },
                show: { opacity: 1, y: 0, transition: { duration: 0.5, ease: 'easeOut' } },
              }}
              whileHover={{ y: -4 }}
              className="text-center p-6"
            >
              <div className={`w-16 h-16 ${iconBg} rounded-full flex items-center justify-center mx-auto mb-4`}>
                <Icon className={`h-8 w-8 ${iconColor}`} />
              </div>
              <h3 className="text-xl font-semibold mb-2">{title}</h3>
              <p className="text-gray-600">{body}</p>
            </motion.div>
          ))}
        </motion.div>
      </div>
    </div>
  );
}