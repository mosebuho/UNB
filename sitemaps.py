from django.contrib.sitemaps import Sitemap
from board.models import Military


class MilSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        results = Military.objects.all()
        return results

    def location(self, obj):
        return f"/mil/%s" % obj.pk

    def lastmod(self, obj):
        return obj.date
