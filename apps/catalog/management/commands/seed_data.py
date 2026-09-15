"""
Demo ma'lumotlar bilan bazani to'ldirish (kategoriya, do'kon, mahsulot).
Ishlatish: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from apps.catalog.models import Category, Market, Product


class Command(BaseCommand):
    help = "Demo kategoriya, do'kon va mahsulotlarni yaratadi"

    def handle(self, *args, **kwargs):
        categories = ["Sabzavotlar", "Mevalar", "Go'sht va baliq", "Non mahsulotlari", "Sut mahsulotlari", "Yog' va moylar", "Ichimliklar", "Shirinliklar"]
        cat_objs = [Category.objects.get_or_create(name=c)[0] for c in categories]

        markets_data = [
            {"name": "Makro (Chilonzor)", "address": "Chilonzor tumani, Toshkent", "rating": 4.8},
            {"name": "Korzinka (Yunusobod)", "address": "Yunusobod tumani, Toshkent", "rating": 4.5},
            {"name": "The Fresh Market", "address": "Mirzo Ulug'bek tumani, Toshkent", "rating": 4.7},
            {"name": "Olcha Market", "address": "Yashnobod tumani, Toshkent", "rating": 4.6},
            {"name": "Green House", "address": "Sergeli tumani, Toshkent", "rating": 4.9},
        ]
        market_objs = [Market.objects.get_or_create(name=m["name"], defaults=m)[0] for m in markets_data]

        products_data = [
            ("Pomidor", "kg", 12900), ("Banan", "kg", 14900), ("Tovuq go'shti", "kg", 34900),
            ("Sut 3.2%", "litr", 12800), ("Non", "dona", 4000), ("Olma", "kg", 9900),
            ("Kartoshka", "kg", 4500), ("Tuxum (o'nlik)", "dona", 22000),
        ]
        for name, unit, price in products_data:
            for market in market_objs[:2]:
                Product.objects.get_or_create(
                    name=name, market=market,
                    defaults={"price": price, "unit": unit, "category": cat_objs[0], "stock": 100},
                )

        self.stdout.write(self.style.SUCCESS("Demo ma'lumotlar muvaffaqiyatli qo'shildi!"))
