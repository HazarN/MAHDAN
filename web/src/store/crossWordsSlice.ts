import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { LegalEntry, legalTerms } from './crossWords';

type LegalState = {
  entries: LegalEntry[];
  userInputs: Record<string, string>;
};

const initialState: LegalState = {
  entries: legalTerms,
  userInputs: {},
};

const legalSlice = createSlice({
  name: 'legal',
  initialState,
  reducers: {
    setUserInput: (
      state,
      action: PayloadAction<{ id: string; value: string }>,
    ) => {
      state.userInputs[action.payload.id] = action.payload.value.toUpperCase();
    },
  },
});

export const { setUserInput } = legalSlice.actions;
export default legalSlice.reducer;
