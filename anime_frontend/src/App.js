import React from "react";
import { BrowserRouter } from "react-router-dom";
import Navbar from "./components/Navbar";
import AppRouter from "./router/AppRouter";
import { AuthProvider } from "./context/AuthContext";
import "./styles/App.css";

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Navbar />
        <div className="container">
          <AppRouter />
        </div>
      </BrowserRouter>
    </AuthProvider>
  );
}
