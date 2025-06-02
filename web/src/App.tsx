import { lazy, Suspense } from 'react';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import LoadingSpinner from './components/LoadingSpinner';

const CaseStudy = lazy(() => import('./pages/CaseStudy'));
const Home = lazy(() => import('./pages/Home'));
const Demo = lazy(() => import('./pages/Demo'));
const Hangman = lazy(() => import('./pages/Hangman'));
const CrossWords = lazy(() => import('./pages/CrossWords'));
const Error = lazy(() => import('./pages/Error'));

const browserRouter = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
  {
    path: '/demo',
    children: [
      {
        path: 'video',
        element: <Demo />,
      },
      {
        path: 'case',
        element: <CaseStudy />,
      },
    ],
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

function App() {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <RouterProvider router={browserRouter} />
    </Suspense>
  );
}
export default App;
