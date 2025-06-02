import { useRef, useState } from 'react';
import ReactPlayer from 'react-player';

const VideoPlayer = () => {
  const playerRef = useRef<ReactPlayer>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [played, setPlayed] = useState(0);

  return (
    <div className="max-w-7xl p-4 bg-gray-900 rounded-xl shadow-lg">
      <div className="aspect-video">
        <ReactPlayer
          ref={playerRef}
          url="/videos/tubitak_compressed.mp4"
          playing={isPlaying}
          controls={false}
          width="100%"
          height="100%"
          onProgress={({ played }) => setPlayed(played)}
          progressInterval={200}
        />
      </div>

      <div className="flex items-center mt-4 space-x-4">
        <button
          className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={() => setIsPlaying(!isPlaying)}
        >
          {isPlaying ? 'Pause' : 'Play'}
        </button>

        <input
          type="range"
          min={0}
          max={1}
          step={0.01}
          value={played}
          onChange={(e) => {
            const value = parseFloat(e.target.value);
            playerRef.current?.seekTo(value);
            setPlayed(value);
          }}
          className="w-full"
        />
      </div>
    </div>
  );
};

export default VideoPlayer;
