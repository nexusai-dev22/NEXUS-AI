import { BrowserRouter, Routes, Route } from "react-router-dom";

import Sidebar from "./components/Sidebar";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Chat from "./pages/Chat";
import Robots from "./pages/Robots";
import Vision from "./pages/Vision";
import Projects from "./pages/Projects";
import Settings from "./pages/Settings";

import "./App.css";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route path="/login" element={<Login />} />

        <Route
          path="/*"
          element={
            <div className="app">
              <Sidebar />

              <main className="contenido">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/chat" element={<Chat />} />
                  <Route path="/robots" element={<Robots />} />
                  <Route path="/vision" element={<Vision />} />
                  <Route path="/projects" element={<Projects />} />
                  <Route path="/settings" element={<Settings />} />
                </Routes>
              </main>
            </div>
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;
