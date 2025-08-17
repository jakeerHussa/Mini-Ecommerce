
#  Mini Ecommerce

A **full-stack e-commerce application** built with:  
- **Django REST Framework** → Backend APIs  
- **React** → Frontend  
- **PostgreSQL → Database  
- **JWT Authentication (SimpleJWT)** → Secure login/logout  
- **Docker & Docker Compose** → Containerized deployment  

The app includes:  
✅ User registration & login (JWT)  
✅ Product & category management  
✅ Cart functionality (add/update/remove)  
✅ Place & view orders  
✅ Order receipt (PDF) download  
✅ Admin role-based restrictions  
✅ Postman collection for API testing  

---

## Project Structure
mini_ecommerce/
│── backend/                 # Django REST API
│── frontend/                # React frontend
│── docker-compose.yml       # Docker setup
│── .env.example             # Example environment variables
│── postman_collection.json  # Postman APIs
│── README.md                # Project documentation


## Tech Stack
- **Backend:** Django, Django REST Framework, SimpleJWT  
- **Frontend:** React, Axios, React Router  
- **Database:** PostgreSQL (via Docker) / SQLite (local dev)  
- **Auth:** JWT (access + refresh tokens) with blacklist support  
- **Containerization:** Docker & Docker Compose  

---


##  Setup & Installation

###  Option 1: Run Locally

1. Clone the repo
   git clone https://github.com/jakeerHussa/Mini-Ecommerce.git
   cd mini_ecommerce

2. Backend (Django)
   cd backend
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt

   # Run migrations & start server
   python manage.py migrate
   python manage.py runserver

    API runs on: http://localhost:8000/

3. Frontend (React)
   cd frontend
   npm install
   npm start

    Frontend runs on: http://localhost:5173/

###  Option 2: Run with Docker

   docker compose up --build

- Backend → http://localhost:8000/  
- Frontend → http://localhost:5173/  
- Database → `db` service inside Docker  

---

##  API Documentation

###  Authentication
POST   /api/auth/register/       → Register new user  
POST   /api/auth/token/          → Login → get access & refresh tokens  
POST   /api/auth/token/refresh/  → Get new access token  
GET    /api/auth/profile/        → Get user profile (JWT required)  

###  Products
GET    /api/products/            → List all products  
POST   /api/products/            → Create product (admin/owner)  
GET    /api/products/{id}/       → Get product details  
PUT    /api/products/{id}/       → Update product (admin/owner)  
DELETE /api/products/{id}/       → Delete product (admin/owner)  

###  Categories
GET    /api/categories/          → List categories  
POST   /api/categories/          → Create category (admin only)  
GET    /api/categories/{id}/     → Category details  
PUT    /api/categories/{id}/     → Update category  
DELETE /api/categories/{id}/     → Delete category  

###  Cart
GET    /api/cart/                → View cart items  
POST   /api/cart/add/            → Add product to cart  
PUT    /api/cart/update/{id}/    → Update cart item quantity  
DELETE /api/cart/remove/{id}/    → Remove item from cart  

###  Orders
GET    /api/orders/              → List user’s orders  
POST   /api/orders/              → Place a new order  
GET    /api/orders/{id}/         → Order details  
GET    /api/orders/{id}/receipt.pdf → Download order receipt (PDF)  

---

## Postman Collection
File: postman_collection.json  

Steps:  
1. Open Postman → Import → Upload `postman_collection.json`  
2. Login first (`/api/auth/token/`) to get JWT  
3. Set `{{token}}` variable in Postman  
4. Use it for Products, Cart, Orders requests  

---

## Running Tests
cd backend
pytest

