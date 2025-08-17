// App.jsx
import React from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route, Link, Navigate } from "react-router-dom";
import Products from "./pages/Products.jsx";
import ProductDetail from "./pages/ProductDetail.jsx";
import Cart from "./pages/Cart.jsx";
import Checkout from "./pages/Checkout.jsx";
import Login from "./pages/Login.jsx";
import Signup from "./pages/Signup.jsx";
import Orders from "./pages/Orders.jsx";

function App() {
  // Keep token in React state
  const [token, setToken] = React.useState(localStorage.getItem("token"));

  // Save token to localStorage whenever it changes
  const login = (newToken) => {
    localStorage.setItem("token", newToken);
    setToken(newToken);
  };

  const logout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <BrowserRouter>
      <div style={{ maxWidth: 900, margin: "0 auto", padding: 16 }}>
        <header style={{ display: "flex", gap: 12, alignItems: "center" }}>
          <Link to="/">Store</Link>
          <Link to="/cart">Cart</Link>
          <Link to="/orders">Orders</Link>
          <div style={{ marginLeft: "auto" }}>
            {token ? (
              <button onClick={logout}>Logout</button>
            ) : (
              <Link to="/login">Login</Link>
            )}
          </div>
        </header>
        <Routes>
          <Route path="/" element={<Products />} />
          <Route path="/products/:id" element={<ProductDetail />} />
          <Route path="/cart" element={<Cart />} />
          <Route
            path="/checkout"
            element={token ? <Checkout /> : <Navigate to="/login" />}
          />
          <Route
            path="/orders"
            element={token ? <Orders /> : <Navigate to="/login" />}
          />
          {/* pass login function to Login so it can set token */}
          <Route path="/login" element={<Login onLogin={login} />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

createRoot(document.getElementById("root")).render(<App />);
