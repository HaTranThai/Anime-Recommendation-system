import axiosClient from "./axiosClient";

export const userApi = {
  register: (data) => axiosClient.post("register/", data),
  login: (data) => axiosClient.post("login/", data),
  logout: (refresh) => axiosClient.post("logout/", { refresh }),
  getProfile: () => axiosClient.get("user/"),
  updateProfile: (data) => axiosClient.put("user/update/", data),
  changePassword: (data) => axiosClient.put("change-password/", data),
};
