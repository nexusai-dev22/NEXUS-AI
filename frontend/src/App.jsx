import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import "./App.css";

function App() {
  return (
    <div className="app">
      <Sidebar />

      <main className="contenido">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
