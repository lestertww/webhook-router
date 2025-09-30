export default function DashboardPage() {
  return (
    <main className="min-h-screen p-10 bg-gray-50">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <p className="mt-2 text-gray-600">Your webhook routers and logs will appear here.</p>
      
      {/* Placeholder for routers */}
      <div className="mt-6 space-y-4">
        <div className="p-4 border rounded shadow-sm">Router 1: Example Router</div>
        <div className="p-4 border rounded shadow-sm">Router 2: Example Router</div>
      </div>
    </main>
  );
}
