import { ReactNode } from 'react';
import Navbar from './Navbar';

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-gradient-to-tl from-[#237562] to-white">
      <Navbar />

      {children}
    </div>
  );
}
