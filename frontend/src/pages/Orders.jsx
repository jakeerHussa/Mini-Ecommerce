import React, { useEffect, useState } from "react";

function Orders() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");
    fetch("http://localhost:8000/api/orders/", {
      headers: {
        "Authorization": `Bearer ${token}`,
        "Content-Type": "application/json"
      }
    })
      .then(res => {
        if (!res.ok) throw new Error("Failed to load orders");
        return res.json();
      })
      .then(data => {
        setOrders(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Loading orders...</p>;
  if (error) return <p style={{color:"red"}}>{error}</p>;
  if (orders.length === 0) return <p>No orders yet.</p>;

 const downloadReceipt = async (orderId) => {
  const token = localStorage.getItem("token");

  const res = await fetch(`http://localhost:8000/api/orders/${orderId}/receipt.pdf`, {
    headers: {
      "Authorization": `Bearer ${token}`,
    },
  });

  if (!res.ok) {
    alert("Failed to download receipt");
    return;
  }

  const blob = await res.blob();
  const url = window.URL.createObjectURL(blob);

  // Create a link & trigger download
  const a = document.createElement("a");
  a.href = url;
  a.download = `order_${orderId}_receipt.pdf`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  window.URL.revokeObjectURL(url);
};

  return (
    <div>
      <h2>Your Orders</h2>
      {orders.map(order => (
        <div key={order.id} style={{border:"1px solid #ddd", padding:12, marginBottom:12, borderRadius:8}}>
          <p><strong>Order #{order.id}</strong></p>
          <p>Status: {order.status}</p>
          <p>Total: ${order.total_amount}</p>
          <p>Date: {new Date(order.created_at).toLocaleString()}</p>
          <ul>
            {order.items.map(item => (
              <li key={item.id}>
                {item.product_name} × {item.quantity} (${item.price})
              </li>
            ))}
          </ul>
          <button onClick={() => downloadReceipt(order.id)}>Download Receipt (PDF)</button>
        </div>
      ))}
    </div>
  );
}

export default Orders;
