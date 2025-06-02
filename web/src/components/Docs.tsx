import { Link } from 'react-router-dom';

function Docs() {
  return (
    <div className="flex  flex-col justify-between col-span-3 bg-white shadow-lg rounded-xl h-full p-6">
      <div>
        <h2 className="text-xl font-semibold mb-4 text-gray-800">Belgeler</h2>
        <ul className="space-y-3">
          <li>
            <a
              href="/pdfs/disiplin_yonetmeligi.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Öğrenci Disiplin Yönetmeliği
            </a>
          </li>
          <li>
            <a
              href="/pdfs/turk_ceza_kanunu.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Türk Ceza Kanunu
            </a>
          </li>
        </ul>
      </div>

      <div className="mt-6 flex justify-end">
        <Link
          to={'/demo/case'}
          className="px-4 py-2 bg-black text-white rounded hover:bg-gray-800"
        >
          Devam Et
        </Link>
      </div>
    </div>
  );
}

export default Docs;
