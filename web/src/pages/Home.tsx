import Card from '../components/Card';
import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <div className="flex items-center justify-center h-screen">
        <div className="flex space-x-4">
          <Card />
          <Card />
          <Card />
        </div>
      </div>
    </Layout>
  );
}
