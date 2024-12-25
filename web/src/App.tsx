import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import CrossWords from './pages/CrossWords';
import Demo from './pages/Demo';
import Error from './pages/Error';
import Hangman from './pages/Hangman';
import Home from './pages/Home';

const browserRouter = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/demo',
    element: <Demo />,
  },
  {
    path: '/mini-games',
    children: [
      {
        path: 'hang-man',
        element: <Hangman />,
      },
      {
        path: 'cross-words',
        element: <CrossWords />,
      },
    ],
  },
  {
    path: '*',
    element: <Error />,
  },
]);

const App = () => <RouterProvider router={browserRouter} />;
export default App;
