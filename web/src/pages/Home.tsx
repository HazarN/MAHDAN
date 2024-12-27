import Card from '../components/Card';
import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <div className="flex items-center justify-center h-screen">
        <div className="grid gap-10 sm:grid-cols-1 md:grid-cols-3 items-center">
          <Card />
          <Card />
          <Card />
        </div>
      </div>
    </Layout>
  );
}
