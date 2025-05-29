import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface HangmanState {
  word: string;
  guessedLetters: string[];
  remainingGuesses: number;
  gameStatus: 'playing' | 'won' | 'lost';
}

const initialState: HangmanState = {
  word: '',
  guessedLetters: [],
  remainingGuesses: 6,
  gameStatus: 'playing',
};

const hangmanSlice = createSlice({
  name: 'hangman',
  initialState,
  reducers: {
    startGame: (state, action: PayloadAction<string>) => {
      state.word = action.payload.toLowerCase();
      state.guessedLetters = [];
      state.remainingGuesses = 6;
      state.gameStatus = 'playing';
    },
    guessLetter: (state, action: PayloadAction<string>) => {
      const letter = action.payload.toLowerCase();

      if (!state.guessedLetters.includes(letter)) {
        state.guessedLetters.push(letter);

        if (!state.word.includes(letter)) {
          state.remainingGuesses -= 1;
        }

        const isWon = state.word
          .split('')
          .every((letter) => state.guessedLetters.includes(letter));

        if (isWon) {
          state.gameStatus = 'won';
        } else if (state.remainingGuesses === 0) {
          state.gameStatus = 'lost';
        }
      }
    },
  },
});

export const { startGame, guessLetter } = hangmanSlice.actions;
export default hangmanSlice.reducer;
