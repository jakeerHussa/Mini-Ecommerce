import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";

export default function Products(){
  const [data, setData] = useState([]);
  useEffect(()=>{
    api.get("/api/products/").then(res=> setData(res.data));
  },[]);
  return (
    <div>
      <h2>Products</h2>
      <div style={{display:"grid", gridTemplateColumns:"repeat(3, 1fr)", gap:12}}>
        {data.map(p => (
          <div key={p.id} style={{border:"1px solid #eee", padding:12, borderRadius:8}}>
            <h3><Link to={`/products/${p.id}`}>{p.name}</Link></h3>
            <p>${p.price}</p>
            <Link to={`/products/${p.id}`}>View</Link>
          </div>
        ))}
      </div>
    </div>
  )
}
