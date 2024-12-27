import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-black text-white p-4 shadow-md">
      <div className="flex justify-between items-center">
        <Link to={'/'} className="text-3xl uppercase tracking-widest">
          Mahdan
        </Link>

        <Link
          to={'/demo'}
          className="bg-white text-black px-4 py-2 rounded-md hover:bg-gray-200 transition-all"
        >
          Demoyu İncele
        </Link>
      </div>
    </nav>
  );
}
