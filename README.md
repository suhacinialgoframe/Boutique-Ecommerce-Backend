# 🛍️ Boutique E-Commerce Backend

## 📌 Project Overview

This project is a RESTful backend API for a Boutique E-Commerce application developed using **FastAPI** and **MongoDB**. It provides APIs for managing products, categories, customers, shopping carts, orders, payments, authentication, reporting, searching, statistics, pagination, and sorting.

The project demonstrates CRUD operations, MongoDB Aggregation Pipelines, `$lookup` joins, authentication, reporting, and advanced backend development concepts.

---

# 🚀 Features

## Authentication

* User Registration
* User Login

## Product Management

* Add Product
* View Products
* Get Product by ID
* Update Product
* Delete Product

## Category Management

* Add Category
* View Categories
* Update Category
* Delete Category

## Customer Management

* Add Customer
* View Customers
* Update Customer
* Delete Customer

## Shopping Cart

* Add to Cart
* View Cart
* Remove Cart Items

## Order Management

* Place Order
* View Orders
* Update Order Status
* Track Order

## Payment Management

* Make Payment
* View Payments
* Update Payment Status

## Reports

* Total Sales Report
* Order Count Report

## Dashboard

* Inventory Dashboard
* Low Stock Products
* Revenue Summary

## MongoDB Aggregation

* Customer Order Lookup
* Customer → Orders → Products Lookup
* Revenue Aggregation
* Statistics

## Search

* Search Products by Name
* Search Products by Price Range

## Pagination & Sorting

* Product Pagination
* Sort by Price
* Sort by Stock
* Sort by Name

---

# 🛠 Tech Stack

* Python 3
* FastAPI
* MongoDB
* PyMongo
* Docker
* Uvicorn
* Swagger UI

---

# 📂 Project Structure

```text
boutique-backend/
│
├── app/
│   ├── database/
│   ├── models/
│   ├── routes/
│   └── main.py
│
├── infra/
│
├── README.md
│
└── venv/
```

---

# ▶️ How to Run

## 1. Activate Virtual Environment

### macOS/Linux

```bash
source venv/bin/activate
```

---

## 2. Run FastAPI

```bash
uvicorn app.main:app --reload
```

---

## 3. Open Swagger UI

```text
http://127.0.0.1:8000/docs
```

---

# 🗄 Database

* MongoDB
* Collections:

  * Products
  * Categories
  * Customers
  * Cart
  * Orders
  * Payments

---

# 📊 API Modules

* Authentication
* Products
* Categories
* Customers
* Cart
* Orders
* Payments
* Aggregation
* Lookup
* Advanced Lookup
* Reports
* Dashboard
* Order Management
* Statistics
* Search
* Pagination & Sorting

---

# 🔮 Future Enhancements

* JWT Token Authentication
* Role-Based Access Control
* Email Notifications
* Image Upload
* Product Reviews
* Wishlist
* Discount Coupons
* Payment Gateway Integration

---

# 👩‍💻 Author

**Suha cini**

Information Technology Student

Boutique E-Commerce Backend Project using FastAPI & MongoDB.
