import AnimeCard from "../components/AnimeCard";

export default function Home({ animes }) {
  return (
    <div className="anime-grid">
      {animes.map((anime) => (
        <AnimeCard key={anime.id} anime={anime} />
      ))}
    </div>
  );
}
