import axiosClient from "./axiosClient";

export const animeApi = {
  list: () => axiosClient.get("anime/"),
  detail: (id) => axiosClient.get(`anime/${id}/`),
  add: (data) => axiosClient.post("anime/add/", data),
  addToWatchHistory: (id, token) =>
    axiosClient.post(`user/watchlist/add/${id}/`, {}, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }),
  recommend: (token, top_n = 3) =>
    axiosClient.get(`recommend/?top_n=${top_n}`, {
      headers: { Authorization: `Bearer ${token}` },
    }),
};


