import React, { useState } from "react";
import { userApi } from "../api/userApi";
import "../styles/Register.css"; // thêm file CSS riêng (hoặc tái sử dụng Login.css)

export default function Register() {
  const [form, setForm] = useState({
    email: "",
    password: "",
    full_name: "",
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await userApi.register(form);
      alert("Đăng ký thành công! Hãy đăng nhập.");
      window.location.href = "/login";
    } catch {
      alert("Đăng ký thất bại! Kiểm tra lại thông tin.");
    }
  };

  return (
    <div className="register-container">
      <div className="register-card">
        <h2 className="register-title">
          <span className="register-icon">📝</span> Đăng ký
        </h2>

        <form onSubmit={handleSubmit} className="register-form">
          <input
            type="text"
            placeholder="Họ và tên"
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          />
          <input
            type="email"
            placeholder="Email"
            onChange={(e) => setForm({ ...form, email: e.target.value })}
          />
          <input
            type="password"
            placeholder="Mật khẩu"
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <button type="submit">Đăng ký</button>
        </form>

        <p className="login-text">
          Đã có tài khoản? <a href="/login">Đăng nhập</a>
        </p>
      </div>
    </div>
  );
}
