import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";

export default function Cart(){
  const [cart, setCart] = useState({items:[]});
  const token = localStorage.getItem("token");
  useEffect(()=>{
    if(token){
      api.get("/api/cart/").then(res=> setCart(res.data));
    }
  },[token]);
  const updateQty = async (itemId, quantity) => {
    await api.patch(`/api/cart/items/${itemId}/`, { quantity });
    const res = await api.get("/api/cart/");
    setCart(res.data);
  };
  const removeItem = async (itemId) => {
    await api.delete(`/api/cart/items/${itemId}/`);
    const res = await api.get("/api/cart/");
    setCart(res.data);
  };
  const total = cart.items.reduce((a, i)=> a + Number(i.product.price) * i.quantity, 0);
  return (
    <div>
      <h2>Cart</h2>
      {!token && <p>Please <Link to="/login">login</Link> to manage your cart.</p>}
      <ul>
        {cart.items.map(i => (
          <li key={i.id} style={{marginBottom:8}}>
            {i.product.name} - ${i.product.price} x {i.quantity}
            <button onClick={()=>updateQty(i.id, i.quantity+1)} style={{marginLeft:8}}>+</button>
            <button onClick={()=>updateQty(i.id, Math.max(1, i.quantity-1))} style={{marginLeft:4}}>-</button>
            <button onClick={()=>removeItem(i.id)} style={{marginLeft:8}}>Remove</button>
          </li>
        ))}
      </ul>
      <p><b>Total:</b> ${total.toFixed(2)}</p>
      {token && cart.items.length>0 && <Link to="/checkout"><button>Checkout</button></Link>}
    </div>
  )
}
