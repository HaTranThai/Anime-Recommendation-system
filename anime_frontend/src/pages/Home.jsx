import React, { useEffect, useState } from "react";
import { animeApi } from "../api/animeApi";
import AnimeCard from "../components/AnimeCard";

export default function Home() {
  const [animes, setAnimes] = useState([]);

  useEffect(() => {
    const fetch = async () => {
      const res = await animeApi.list();
      setAnimes(res.data);
    };
    fetch();
  }, []);

  return (
    <div>
      <div className="grid">
        {animes.map((a) => (
          <AnimeCard key={a.id} anime={a} />
        ))}
      </div>
    </div>
  );
}
