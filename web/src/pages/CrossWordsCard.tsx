import { useDispatch, useSelector } from 'react-redux';

import { setUserInput } from '../store/crossWordsSlice';
import { RootState } from '../store/store';

type Props = {
  id: string;
  category: string;
  definition: string;
  length: number;
};

const CrossWordsCard = ({ id, category, definition, length }: Props) => {
  const dispatch = useDispatch();
  const value = useSelector(
    (state: RootState) => state.crossWords.userInputs[id] || '',
  );

  return (
    <div className="mb-6 border p-4 rounded-lg bg-white shadow">
      <p className="text-sm text-gray-500 mb-1">{category}</p>
      <p className="text-gray-800 mb-2">{definition}</p>
      <input
        type="text"
        value={value}
        onChange={(e) => dispatch(setUserInput({ id, value: e.target.value }))}
        maxLength={length}
        className="border border-gray-300 p-2 w-full uppercase tracking-widest"
      />
    </div>
  );
};

export default CrossWordsCard;
