import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { animeApi } from "../api/animeApi";
import "../styles/AnimeWatch.css";

export default function AnimeWatch() {
  const { id, ep } = useParams();
  const navigate = useNavigate();
  const [anime, setAnime] = useState(null);
  const [episode, setEpisode] = useState(parseInt(ep) || 1);
  const [server, setServer] = useState("VIP 1");

  useEffect(() => {
    const fetchAnime = async () => {
      try {
        const res = await animeApi.detail(id);
        setAnime(res.data);
      } catch (err) {
        console.error("Error fetching anime:", err);
      }
    };
    fetchAnime();
  }, [id]);

  if (!anime) return <div className="loading">Đang tải dữ liệu phim...</div>;

  const totalEpisodes = anime.total_episodes || 170; // ví dụ mặc định
  const handleEpisodeClick = (num) => navigate(`/anime/${id}/watch/${num}`);

  return (
    <div className="watch-container">
      <h2 className="watch-title">
        🎬 {anime.title} — Tập {episode}
      </h2>

      {/* VIDEO PLAYER */}
      <div className="video-wrapper">
        <iframe
          src={anime.video_url || anime.link_anime}
          title={`Tập ${episode}`}
          allowFullScreen
          loading="lazy"
        ></iframe>
      </div>

      {/* NOTICE */}
      <div className="watch-notice">
        <p>
          🕒 <b>Tập {totalEpisodes} </b> sẽ được chiếu <b>18h Thứ Bảy hàng tuần!</b>
        </p>
        <ul>
          <li>
            💡 Lưu ngay địa chỉ <b>recommendanime.localhost</b> để truy cập nhanh nhất!
          </li>
          <li>
            🔄 Nếu lỗi load, hãy thử chọn lại server khác (VIP1 / VIP2 / HYADS).
          </li>
          <li>⚡ Xem tốt nhất trên trình duyệt Chrome, Cốc Cốc hoặc Firefox.</li>
        </ul>
      </div>

      {/* DANH SÁCH TẬP PHIM */}
      <div className="episode-list">
        <h3>📺 Danh sách tập phim</h3>
        <div className="episode-grid">
          {Array.from({ length: totalEpisodes }, (_, i) => (
            <button
              key={i + 1}
              className={`episode-btn ${episode === i + 1 ? "active" : ""}`}
              onClick={() => handleEpisodeClick(i + 1)}
            >
              Tập {i + 1}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
