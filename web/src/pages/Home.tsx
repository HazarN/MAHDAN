import CardGrid from '../components/CardGrid';
import Layout from '../components/Layout';

export default function Home() {
  return (
    <Layout>
      <div className="relative min-h-screen overflow-hidden">
        {/* Semi-elliptical background */}
        <div
          className="absolute sm:top-[-150%] md:top-[-100%] lg:top-[-100%] left-[-25%] right-[-25%] bottom-0 
          bg-black sm:rounded-[50%] md:rounded-[50%] lg:rounded-[50%] transform scale-y-[0.5]"
          style={{ width: '150%' }}
        />

        <div className="relative min-h-screen flex flex-col items-center pt-16 px-4 mt-[10vh]">
          <h1 className="text-4xl p-6 md:text-5xl font-bold text-white text-center mb-12 max-w-4xl">
            MAHDAN | Hukukta Yapay Zeka
          </h1>

          <h6 className="text-3xl text-white text-center mb-12 max-w-4xl">
            Yapay zekanın gücü adaletiyle birleşseydi ne olurdu?
          </h6>

          <div className="mt-[15vh] w-full max-w-7xl">
            <CardGrid />
          </div>
        </div>
      </div>
    </Layout>
  );
}
