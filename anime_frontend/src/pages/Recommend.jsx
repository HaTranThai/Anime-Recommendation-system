import React, { useEffect, useState } from "react";
import { animeApi } from "../api/animeApi";
import AnimeCard from "../components/AnimeCard";
import "../styles/Recommend.css";

export default function RecommendPage() {
  const [recs, setRecs] = useState([]);
  const [loading, setLoading] = useState(false);
  const token = localStorage.getItem("access_token");

  // Hàm gọi API gợi ý
  const handleRecommendClick = async () => {
    if (!token) {
      alert("⚠️ Vui lòng đăng nhập để xem gợi ý phim!");
      return;
    }

    setLoading(true);
    try {
      const res = await animeApi.recommend(token, 10);
      setRecs(res.data); // nhận danh sách gợi ý
    } catch (err) {
      console.error("❌ Lỗi khi lấy gợi ý phim:", err);
      alert("Không thể lấy gợi ý phim!");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="recommend-container">
      <h2
        className="recommend-title"
        onClick={handleRecommendClick}
        style={{ cursor: "pointer" }}
      >
        🎬 Gợi ý phim dành cho bạn
      </h2>

      {loading && <div className="loading">⏳ Đang tải gợi ý...</div>}

      {!loading && recs.length === 0 && (
        <p className="empty">👉 Nhấn vào tiêu đề trên để xem gợi ý phim!</p>
      )}

      {!loading && recs.length > 0 && (
        <div className="grid">
          {recs.map((anime) => (
            <AnimeCard key={anime.anime_code || anime.id} anime={anime} />
          ))}
        </div>
      )}
    </div>
  );
}
