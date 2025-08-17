import React from "react";
import { useNavigate } from "react-router-dom";
import api from "../api";

export default function Signup(){
  const nav = useNavigate();
  const [form, setForm] = React.useState({username:"", email:"", password:""});
  const onSubmit = async (e) => {
    e.preventDefault();
    await api.post("/api/auth/register/", form);
    const r = await api.post("/api/auth/token/", {username: form.username, password: form.password});
    localStorage.setItem("token", r.data.access);
    nav("/");
  };
  return (
    <div>
      <h2>Sign up</h2>
      <form onSubmit={onSubmit} style={{display:"grid", gap:8, maxWidth:320}}>
        <input placeholder="Username" value={form.username} onChange={e=>setForm({...form, username:e.target.value})}/>
        <input placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})}/>
        <input placeholder="Password" type="password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})}/>
        <button type="submit">Create account</button>
      </form>
    </div>
  )
}
