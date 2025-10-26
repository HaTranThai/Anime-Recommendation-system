import React, { useState } from "react";
import { animeApi } from "../api/animeApi";

export default function AnimeAdd() {
  const [form, setForm] = useState({
    title: "",
    description: "",
    genre: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await animeApi.add(form);
      alert("Thêm anime thành công!");
    } catch {
      alert("Lỗi khi thêm anime!");
    }
  };

  return (
    <div className="form-page">
      <h2>Thêm Anime Mới</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Tên phim"
          onChange={(e) => setForm({ ...form, title: e.target.value })}
        />
        <input
          type="text"
          placeholder="Thể loại"
          onChange={(e) => setForm({ ...form, genre: e.target.value })}
        />
        <textarea
          placeholder="Mô tả"
          onChange={(e) => setForm({ ...form, description: e.target.value })}
        />
        <button type="submit">Thêm Anime</button>
      </form>
    </div>
  );
}
