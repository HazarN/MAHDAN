import { useEffect, useState } from 'react';
import Layout from '../components/Layout';
import { LegalCategory, legalTerms } from '../store/crossWords';

type Pair = {
  id: string;
  definition: string;
  term: string;
};

type Match = {
  defId: string;
  termId: string;
};

const categories: LegalCategory[] = [
  'MEDENİ HUKUK',
  'ANAYASA HUKUKU',
  'CEZA HUKUKU',
  'BORÇLAR HUKUKU',
  'İDARE HUKUKU',
];

export default function MatchingGame() {
  const [selectedCategory, setSelectedCategory] =
    useState<LegalCategory | null>(null);
  const [shuffledDefs, setShuffledDefs] = useState<Pair[]>([]);
  const [shuffledTerms, setShuffledTerms] = useState<Pair[]>([]);
  const [selectedDef, setSelectedDef] = useState<string | null>(null);
  const [selectedTerm, setSelectedTerm] = useState<string | null>(null);
  const [matches, setMatches] = useState<Match[]>([]);

  useEffect(() => {
    if (selectedCategory) {
      const filtered = legalTerms
        .filter((item) => item.category === selectedCategory)
        .map(({ id, definition, term }) => ({ id, definition, term }));

      const shuffled = (arr: any[]) => [...arr].sort(() => Math.random() - 0.5);

      setShuffledDefs(shuffled(filtered));
      setShuffledTerms(shuffled(filtered));
      setMatches([]);
      setSelectedDef(null);
      setSelectedTerm(null);
    }
  }, [selectedCategory]);

  useEffect(() => {
    if (selectedDef && selectedTerm) {
      if (selectedDef === selectedTerm) {
        setMatches((prev) => [
          ...prev,
          { defId: selectedDef, termId: selectedTerm },
        ]);
      }
      setTimeout(() => {
        setSelectedDef(null);
        setSelectedTerm(null);
      }, 300);
    }
  }, [selectedDef, selectedTerm]);

  const isMatched = (id: string) =>
    matches.some((m) => m.defId === id || m.termId === id);

  return (
    <Layout>
      {!selectedCategory ? (
        <div className="flex flex-col items-center gap-4 py-8">
          <h2 className="text-2xl font-bold">Kategorini Seç</h2>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
            {categories.map((cat) => (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className="px-4 py-2 bg-black hover:bg-gray-800 text-white rounded-lg shadow"
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      ) : (
        <div className="grid mx-auto m-2 grid-cols-2 gap-8 max-w-5xl w-full">
          {/* Tanımlar */}
          <div className="flex flex-col gap-4">
            <h2 className="text-lg font-semibold text-center">Tanımlar</h2>
            <div className="grid grid-cols-1 gap-4">
              {shuffledDefs.map((item) => (
                <button
                  key={item.id}
                  onClick={() => !isMatched(item.id) && setSelectedDef(item.id)}
                  className={`p-4 h-32 text-[8px] sm:text-[12px] md:text-[14px] lg:text-[16px] border rounded-lg shadow text-sm flex items-center justify-center text-center transition-all duration-150
                  ${
                    isMatched(item.id)
                      ? 'bg-green-200 text-green-800'
                      : selectedDef === item.id
                        ? 'bg-gray-200'
                        : 'bg-white hover:bg-gray-100'
                  }
                `}
                >
                  {item.definition}
                </button>
              ))}
            </div>
          </div>

          {/* Kelimeler */}
          <div className="flex flex-col gap-4">
            <h2 className="text-lg font-semibold text-center">Kelimeler</h2>
            <div className="grid grid-cols-1 gap-4">
              {shuffledTerms.map((item) => (
                <button
                  key={item.id}
                  onClick={() =>
                    !isMatched(item.id) && setSelectedTerm(item.id)
                  }
                  className={`p-4 h-32 border rounded-lg shadow text-sm uppercase tracking-widest flex items-center justify-center text-center transition-all duration-150
                  ${
                    isMatched(item.id)
                      ? 'bg-green-200 text-green-800'
                      : selectedTerm === item.id
                        ? 'bg-gray-200'
                        : 'bg-white hover:bg-gray-100'
                  }
                `}
                >
                  {item.term}
                </button>
              ))}
            </div>
          </div>

          {/* Geri Butonu */}
          <div className="col-span-2 flex justify-center mt-6">
            <button
              onClick={() => setSelectedCategory(null)}
              className="px-4 py-2 bg-black hover:bg-gray-800 text-white rounded-lg"
            >
              Kategoriye Geri Dön
            </button>
          </div>
        </div>
      )}
    </Layout>
  );
}
