import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../api";

export default function ProductDetail(){
  const { id } = useParams();
  const [p, setP] = useState(null);
  const nav = useNavigate();
  useEffect(()=>{
    api.get(`/api/products/${id}/`).then(res=> setP(res.data));
  },[id]);
  const addToCart = async () => {
    await api.post("/api/cart/items/", { product_id: p.id, quantity: 1 });
    nav("/cart");
  };
  if(!p) return <div>Loading...</div>
  return (
    <div>
      <h2>{p.name}</h2>
      <p>${p.price}</p>
      <p>{p.description}</p>
      <button onClick={addToCart}>Add to cart</button>
    </div>
  )
}
