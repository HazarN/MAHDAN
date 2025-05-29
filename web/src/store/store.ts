import { configureStore } from '@reduxjs/toolkit';
import crossWordsReducer from './crossWordsSlice';
import hangmanReducer from './hangmanSlice';

export const store = configureStore({
  reducer: {
    hangman: hangmanReducer,
    crossWords: crossWordsReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
