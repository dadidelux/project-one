import { Link } from 'react-router-dom';
import logo from '../assets/logo.png';

export default function Footer() {
  return (
    <footer className="bg-white border-t mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="flex items-center gap-2">
            <img src={logo} alt="The Data Grounds" className="h-8 w-8" />
            <span className="text-primary-700 font-bold text-lg">The Data Grounds</span>
          </div>

          <nav className="flex gap-6">
            <Link to="/courses" className="text-gray-600 hover:text-gray-900">
              Courses
            </Link>
            <Link to="/my-courses" className="text-gray-600 hover:text-gray-900">
              My Learning
            </Link>
          </nav>

          <p className="text-gray-500 text-sm">
            &copy; {new Date().getFullYear()} The Data Grounds. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
