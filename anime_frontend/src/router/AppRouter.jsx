import { Routes, Route } from "react-router-dom";
import Home from "../pages/Home";
import Login from "../pages/Login";
import Register from "../pages/Register";
import Profile from "../pages/Profile";
import AnimeAdd from "../pages/AnimeAdd";
import AnimeDetail from "../pages/AnimeDetail";
import AnimeWatch from "../pages/AnimeWatch";
import Recommend from "../pages/Recommend";

export default function AppRouter() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route path="/profile" element={<Profile />} />
      <Route path="/anime/add" element={<AnimeAdd />} />
      <Route path="/anime/:id" element={<AnimeDetail />} />
      <Route path="/anime/:id/watch/:ep" element={<AnimeWatch />} />
      <Route path="/recommend" element={<Recommend />} />
    </Routes>
  );
}
