import { ReactNode } from 'react';
import Navbar from './Navbar';

type Props = {
  children: ReactNode;
  inDemo?: boolean | undefined;
};
export default function Layout({ children, inDemo }: Props) {
  return (
    <div className="min-h-screen bg-gradient-to-tl from-[#237562] to-white">
      <Navbar inDemo={inDemo} />

      {children}
    </div>
  );
}
