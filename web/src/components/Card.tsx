export default function Card({
  isMain,
  children,
}: {
  isMain: boolean;
  children: React.ReactNode;
}) {
  const cardCondition = isMain
    ? 'w-[400px] h-[250px] lg:w-[500px] lg:h-[300px]'
    : 'w-[300px] h-[200px] lg:w-[400px] lg:h-[250px]';

  return (
    <div
      className={`flex justify-around flex-col items-center p-6 rounded-lg shadow-md border-t-8 border-black uppercase ${cardCondition}`}
    >
      {children}
    </div>
  );
}
