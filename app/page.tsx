export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 text-gray-900 p-10">
      <h1 className="text-5xl font-bold">Webhook Router</h1>
      <p className="mt-4 text-lg text-gray-600 text-center max-w-xl">
        Route, filter, and forward webhooks effortlessly. Build and manage your webhook routers in one place.
      </p>
      <button className="mt-6 px-6 py-3 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
        Get Started
      </button>
    </main>
  );
}
