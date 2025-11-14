# StockLite POS - Learning Django Signals Through a Mini POS Project

Welcome to **StockLite POS**, a mini Point-of-Sale system built in Django to **practice and master Django Signals**.  

This project is designed as a **hands-on tutorial** where each feature demonstrates a specific **signal usage**, allowing you to understand and implement real-world event-driven logic in Django.

---

## 📚 What You Will Learn

By exploring this project, you will learn:

1. **Django Signals Basics**  
   - `pre_save` / `post_save`  
   - `pre_delete` / `post_delete`  

2. **Advanced Signal Concepts**  
   - Detecting updates and adjusting related models  
   - Triggering custom signals (`stock_empty`)  
   - Logging actions using a dedicated model (`ActivityLog`)  

3. **Integrating Signals into Real Use Cases**  
   - Automatically calculating `total_price` for sales  
   - Updating stock dynamically on sale creation, update, or deletion  
   - Preventing invalid operations (selling more than available stock, deleting old sales)  
   - Sending alerts when product stock reaches zero  

4. **Model-Level Best Practices**  
   - Using `save()` overrides vs. signals for critical fields  
   - Combining signals and model logic for robust behavior  

5. **Hands-On Frontend Integration**  
   - Minimal TailwindCSS frontend to test signals  
   - Creating, updating, and deleting sales while observing signal effects  

---

## ⚙️ Features Implemented

| Feature | Signal Used | Purpose |
|---------|------------|---------|
| Auto calculate total price | `pre_save` | Ensures `total_price` is always correct before saving |
| Stock validation before sale | `pre_save` | Blocks sales if quantity > available stock |
| Adjust stock on sale update | `pre_save` | Handles quantity changes correctly |
| Reduce stock on new sale | `post_save` | Updates product stock after sale creation |
| Restore stock on sale delete | `post_delete` | Returns product stock when a sale is removed |
| Prevent deletion of old sales | `pre_delete` | Stops deletion of sales older than 48 hours |
| Logging creation, update, delete | `post_save`, `post_delete` | Records events in `ActivityLog` model |
| Stock empty alert | Custom signal `stock_empty` | Sends alert when product stock reaches zero |

---

## 🏗️ Project Structure

- **stocklite/**
- ├── **core/**
- │ ├── **admin.py**
- │ ├── **apps.py**
- │ ├── **models.py**
- │ ├── **signals.py**
- │ ├── **views.py**
- │ ├── **urls.py**
- │ └── **templates/**
- │ ├── **base.html**
- │ ├── **product_list.html**
- │ ├── **create_sale.html**
- │ └── **sale_list.html**
- ├── **manage.py**
- └── **README.md**
- **models.py** → Contains `Product`, `Sale`, and `ActivityLog` models.  
- **signals.py** → All signal logic for stock updates, logging, and custom signals.  
- **apps.py** → Configured to auto-load signals.  
- **templates/** → Minimal Tailwind frontend to create, update, and delete sales.  

---

## 💡 How Signals Work in This Project

1. **pre_save**  
   - Runs **before saving a model**.  
   - Used for validating stock, calculating `total_price`, and adjusting stock on updates.

2. **post_save**  
   - Runs **after saving a model**.  
   - Used for reducing stock, logging creation/update, and sending custom alerts.

3. **pre_delete**  
   - Runs **before deleting a model**.  
   - Used for blocking deletion of old sales.

4. **post_delete**  
   - Runs **after deleting a model**.  
   - Used for restoring stock and logging deletion.

5. **Custom Signals**  
   - Example: `stock_empty` fires when a product hits zero stock.  
   - Demonstrates **how to create and connect custom signals**.

---

## 📝 How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/yourusername/stocklite-pos.git
cd stocklite-pos
```

2. Create a virtual environment:

```bash
python -m venv env
source env/bin/activate   # Linux / macOS
env\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Make migrations and migrate:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Create a superuser to access admin:

```bash
python manage.py createsuperuser
```

6. Run the development server:

```bash
python manage.py runserver
```

7. Open browser:

```bash
http://127.0.0.1:8000/admin/
http://127.0.0.1:8000/products/
http://127.0.0.1:8000/sales/new/
```

---

## ✅ Conclusion

This project is a hands-on tutorial to learn Django Signals in a practical scenario:

   - You see signals applied to stock management, validation, logging, and alerts.  
   - It teaches both simple and advanced signal techniques.
   - It combines backend logic with a minimal frontend, so you can test everything interactively. 

 
By following this project, you will gain confidence to implement robust, event-driven logic in your Django projects using pre_save, post_save, pre_delete, post_delete, and custom signals.

---


## 👨‍💻 Author
Md Abdullah Al Fahim – Practicing Django, Python, and modern web development.

---
