import Layout from '../components/Layout';
import VideoPlayer from '../components/VideoPlayer';

export default function Demo() {
  return (
    <Layout inDemo={true}>
      <VideoPlayer />
    </Layout>
  );
}
