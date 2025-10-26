import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { animeApi } from "../api/animeApi";
import "../styles/AnimeDetail.css";
import "../styles/AnimePoster.css";

export default function AnimeDetail() {
  const { id } = useParams();
  const [anime, setAnime] = useState(null);
  const navigate = useNavigate();

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

  // 👉 Hàm xử lý khi click "XEM PHIM"
  const handleClick = async () => {
    const token = localStorage.getItem("access_token");
    if (!token) {
      alert("Vui lòng đăng nhập để xem phim!");
      return;
    }

    try {
      await animeApi.addToWatchHistory(anime.id, token);
      console.log(`✅ Đã thêm ${anime.title} vào danh sách đã xem.`);
    } catch (err) {
      console.error("❌ Lỗi khi thêm vào lịch sử xem:", err);
    }

    navigate(`/anime/${anime.id}/watch/1`);
  };

  if (!anime) return <div className="loading">Đang tải thông tin...</div>;

  return (
    <div
      className="anime-detail"
      style={{
        backgroundImage: `linear-gradient(to right, rgba(0,0,0,0.9) 40%, rgba(0,0,0,0.6)), url(${anime.image_link})`,
      }}
    >
      <div className="anime-container">
        {/* ẢNH POSTER */}
        <div className="anime-poster" onClick={handleClick}>
          <div className="poster-wrapper">
            <img
              src={anime.image_link}
              alt={anime.title}
              className="anime-image"
            />

            {/* Icon play giữa ảnh */}
            <div className="play-icon">▶</div>

            {/* Dải băng đỏ XEM PHIM */}
            <div className="banner">XEM PHIM</div>
          </div>
        </div>

        {/* THÔNG TIN */}
        <div className="anime-info">
          <h1 className="anime-title-detail">{anime.title}</h1>
          {anime.subtitle && (
            <h3 className="anime-subtitle">{anime.subtitle}</h3>
          )}

          <p className="anime-description">{anime.description}</p>

          <div className="anime-meta">
            <p>
              <strong>Tập mới:</strong>{" "}
              <span className="tag">{anime.new_episode}</span>
            </p>
            <p>
              <strong>Tập mới nhất:</strong>{" "}
              {anime.latest_episode || "Đang cập nhật..."}
            </p>
            <p>
              <strong>Lịch chiếu:</strong>{" "}
              {anime.release_schedule || "Đang cập nhật..."}
            </p>
            <p>
              <strong>Thể loại:</strong>{" "}
              {anime.genre.split(",").map((g, i) => (
                <span key={i} className="genre-tag">
                  {g.trim()}
                </span>
              ))}
            </p>
            <p>
              <strong>Đạo diễn:</strong> {anime.director || "Đang cập nhật..."}
            </p>
            <p>
              <strong>Quốc gia:</strong> {anime.country || "Không rõ"}
            </p>
            <p>
              <strong>Thời lượng:</strong> {anime.duration || "Không rõ"}
            </p>
            {anime.rating && (
              <p>
                <strong>Đánh giá:</strong>{" "}
                <span className="rating">{anime.rating.toFixed(1)}⭐</span>
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
