import { useNavigate } from "react-router-dom";

export default function AnimeCard({ anime }) {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/anime/${anime.id}`);
  };

  return (
    <div className="anime-card" onClick={handleClick}>
      <div className="image-wrapper">
        <img src={anime.image_link} alt={anime.title} className="anime-image" />

        {/* Góc trái hiển thị rating */}
        {anime.rating && (
          <div className="rating-badge">⭐ {anime.rating.toFixed(1)}</div>
        )}
      </div>

      <h3 className="anime-title">{anime.title}</h3>
      <p className="anime-genre">{anime.genre}</p>
    </div>
  );
}
