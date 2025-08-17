import React from "react";
import { Link, useNavigate } from "react-router-dom";
import api from "../api";

export default function Login({ onLogin }) {
  const nav = useNavigate();
  const [form, setForm] = React.useState({ username: "", password: "" });

  const onSubmit = async (e) => {
    e.preventDefault();
    const res = await api.post("/api/auth/token/", form);
    onLogin(res.data.access);  // update state + localStorage
    nav("/");
  };

  return (
    <div>
      <h2>Login</h2>
      <form
        onSubmit={onSubmit}
        style={{ display: "grid", gap: 8, maxWidth: 320 }}
      >
        <input
          placeholder="Username"
          value={form.username}
          onChange={(e) =>
            setForm({ ...form, username: e.target.value })
          }
        />
        <input
          placeholder="Password"
          type="password"
          value={form.password}
          onChange={(e) =>
            setForm({ ...form, password: e.target.value })
          }
        />
        <button type="submit">Login</button>
      </form>
      <p>
        No account? <Link to="/signup">Sign up</Link>
      </p>
    </div>
  );
}
