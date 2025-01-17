import { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';

import Layout from '../components/Layout';
import wordsList from '../store/handmanWords.json';
import { guessLetter, startGame } from '../store/hangmanSlice';
import { RootState } from '../store/store';

const words = wordsList.words;

export default function Hangman() {
  const dispatch = useDispatch();
  const { word, guessedLetters, remainingGuesses, gameStatus } = useSelector(
    (state: RootState) => state.hangman,
  );

  useEffect(() => {
    const randomWord = words[Math.floor(Math.random() * words.length)];
    dispatch(startGame(randomWord));
  }, [dispatch]);

  // for keyboard events
  useEffect(() => {
    const regex = /^[a-zçğıöşü]$/;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (gameStatus === 'playing' && e.key.match(regex)) {
        handleGuess(e.key);
      }
    };
    window.addEventListener('keydown', handleKeyDown);

    return () => window.removeEventListener('keydown', handleKeyDown);
  });

  function handleGuess(letter: string) {
    if (gameStatus === 'playing') {
      dispatch(guessLetter(letter));
    }
  }

  const displayWord = word
    .split('')
    .map((letter) => (guessedLetters.includes(letter) ? letter : '_'))
    .join(' ');

  const alphabet = 'abcçdefgğhıijklmnoöprsştuüvyz'.split('');

  return (
    <Layout>
      <div className="flex flex-col items-center justify-center min-h-[80vh] p-4">
        <div className="text-4xl font-bold mb-8">{displayWord}</div>

        <div className="mb-4">Kalan Hak: {remainingGuesses}</div>

        <div className="grid grid-cols-7 gap-2 max-w-md">
          {alphabet.map((letter) => (
            <button
              key={letter}
              onClick={() => handleGuess(letter)}
              disabled={
                guessedLetters.includes(letter) || gameStatus !== 'playing'
              }
              className={`w-10 h-10 rounded-md text-center lowercase font-bold
                ${
                  guessedLetters.includes(letter)
                    ? 'bg-gray-300 cursor-not-allowed'
                    : 'bg-black text-white hover:bg-gray-800'
                }
              `}
            >
              {letter}
            </button>
          ))}
        </div>

        {gameStatus !== 'playing' && (
          <div className="mt-8 text-2xl font-bold">
            {gameStatus === 'won' ? 'Tebrikler! Kazandınız!' : 'Oyun Bitti!'}
            <button
              onClick={() => {
                const randomWord =
                  words[Math.floor(Math.random() * words.length)];
                dispatch(startGame(randomWord));
              }}
              className="mt-4 bg-black text-white px-6 py-2 rounded-md hover:bg-gray-800"
            >
              Yeniden Oyna
            </button>
          </div>
        )}
      </div>
    </Layout>
  );
}
