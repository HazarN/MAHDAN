const LoadingSpinner = () => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-white">
      <div className="h-12 w-12 animate-spin rounded-full border-4 border-gray-300 border-t-gray-800"></div>
    </div>
  );
};

export default LoadingSpinner;
