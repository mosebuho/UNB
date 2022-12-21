from django.views import generic
from board.models import Military


class IndexView(generic.ListView):
    template_name = "index.html"
    paginate_by = 25

    def get_queryset(self):
        s = self.request.GET.get("s", "")
        z = self.request.GET.get("z", "")
        if z == "":
            if s == "":
                queryset = Military.objects.all()
            else:
                queryset = Military.objects.filter(category=s)
        else:
            if s == "W":
                queryset = Military.objects.filter(title__contains=z)
            else:
                queryset = Military.objects.filter(category=s, title__contains=z)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["z"] = self.request.GET.get("z", "")
        context["s"] = self.request.GET.get("s", "")
        return context
