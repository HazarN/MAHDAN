import Docs from '../components/Docs';
import Layout from '../components/Layout';
import VideoPlayer from '../components/VideoPlayer';

export default function Demo() {
  return (
    <Layout inDemo={true}>
      <div className="flex flex-col gap-4 lg:flex-row md:flex-row sm:flex-row justify-center p-4">
        <div className="col-span-7">
          <VideoPlayer />
        </div>

        <div className="col-span-3">
          <Docs />
        </div>
      </div>
    </Layout>
  );
}
