# Shopix — Backend (Django + DRF)

Bu — Shopix onlayn market loyihasining backend qismi. Django REST Framework orqali
React frontend uchun API beradi (Uzum Market / Olcha.uz uslubida).

## O'rnatish

```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser   # admin panel uchun
python manage.py seed_data         # demo mahsulotlar (ixtiyoriy)
python manage.py runserver
```

Server: **http://127.0.0.1:8000**
Django admin: **http://127.0.0.1:8000/admin/**

## Asosiy API endpointlar

| Amal | Method & URL |
|---|---|
| Ro'yxatdan o'tish | `POST /api/accounts/register/` |
| Login (JWT) | `POST /api/accounts/login/` |
| Token yangilash | `POST /api/accounts/login/refresh/` |
| Profil | `GET/PATCH /api/accounts/profile/` |
| Saqlangan kartalar | `GET/POST /api/accounts/cards/` |
| Kategoriyalar | `GET /api/catalog/categories/` |
| Do'konlar | `GET /api/catalog/markets/` |
| Mahsulotlar | `GET /api/catalog/products/?search=&category=&market=&ordering=` |
| Mahsulot izohlari | `GET/POST /api/catalog/reviews/?product=<id>` |
| Savatcha | `GET /api/orders/cart/` |
| Savatga qo'shish | `POST /api/orders/cart/add/` |
| Savat elementini o'zgartirish/o'chirish | `PATCH/DELETE /api/orders/cart/items/<id>/` |
| Buyurtma rasmiylashtirish (checkout) | `POST /api/orders/checkout/` |
| Mening buyurtmalarim | `GET /api/orders/orders/` |
| Buyurtma statusini o'zgartirish (admin) | `PATCH /api/orders/orders/<id>/status/` |
| Admin dashboard statistikasi | `GET /api/analytics/dashboard/` |

Barcha himoyalangan endpointlar uchun header:
`Authorization: Bearer <access_token>`
