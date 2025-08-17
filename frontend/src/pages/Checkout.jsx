import React from "react";
import api from "../api";

export default function Checkout(){
  const [result, setResult] = React.useState(null);
  const pay = async () => {
    const res = await api.post("/api/orders/checkout/");
    setResult(res.data);
  };
  return (
    <div>
      <h2>Checkout</h2>
      <button onClick={pay}>Pay (Mock)</button>
      {result && (
        <div style={{marginTop:12}}>
          <p>Order #{result.id} placed. Total ${result.total}</p>
        </div>
      )}
    </div>
  )
}
