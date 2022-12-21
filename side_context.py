from board.models import Military
from datetime import date, timedelta


def side_context(request):
    today = date.today()
    ago = today - timedelta(days=3)
    return {
        "hot": Military.objects.filter(date__date__range=(ago, today)).order_by(
            "-score"
        )[:10]
    }
