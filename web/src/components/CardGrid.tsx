import { Link } from 'react-router-dom';
import Card from './Card';

export default function CardGrid() {
  return (
    <div className="grid gap-60 sm:gap-10 md:gap-20 lg:gap-30 sm:grid-cols-1 md:grid-cols-3 place-items-center">
      <Card isMain={false}>
        <h2 className="text-xl font-semibold mb-2">Mini oyun</h2>

        <Link
          to={'/mini-games/hang-man'}
          className="uppercase bg-black text-white px-4 py-2 rounded-md"
        >
          Adam Asmaca
        </Link>
      </Card>

      <Card isMain={true}>
        <h2 className="text-xl font-semibold mb-2">
          Demo uygulamayı inceleyin
        </h2>

        <Link
          to={'/demo'}
          className="uppercase bg-black text-white px-4 py-2 rounded-md"
        >
          Demo'yu Incele
        </Link>
      </Card>

      <Card isMain={false}>
        <h2 className="text-xl font-semibold mb-2">Mini oyun</h2>
        <Link
          to={'/mini-games/cross-words'}
          className="uppercase bg-black text-white px-4 py-2 rounded-md"
        >
          Kelime Eşleştirme
        </Link>
      </Card>
    </div>
  );
}
