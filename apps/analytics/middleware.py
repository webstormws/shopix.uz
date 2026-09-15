"""
Har bir so'rovni (asosan sahifa/GET so'rovlarini) avtomatik ravishda Visit jadvaliga yozib boruvchi middleware.
Bu orqali admin panelda "nechta odam kirgani / foydalanganini" hisoblaymiz.
"""


class VisitLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # admin va statik fayllarni hisoblamaymiz, faqat API so'rovlarini yozamiz
        if request.path.startswith("/api/") and request.method == "GET":
            try:
                from .models import Visit  # apps tayyor bo'lgach import qilinadi (AppRegistryNotReady oldini olish)
                Visit.objects.create(
                    path=request.path,
                    ip_address=request.META.get("REMOTE_ADDR"),
                    user=request.user if request.user.is_authenticated else None,
                )
            except Exception:
                pass  # migratsiya bo'lmagan holatda xatolik bermasligi uchun

        return response