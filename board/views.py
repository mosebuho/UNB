from django.urls import reverse_lazy
from .forms import MilitaryModelForm
from django.views import generic
from django.http import JsonResponse
from .models import Military, Comment, Image
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import Http404


class MilitaryCreateView(generic.CreateView):
    template_name = "form.html"
    form_class = MilitaryModelForm

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404("글을 생성할 권한이 없습니다.")
        return super(MilitaryCreateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:mil_detail", kwargs={"pk": self.object.pk})

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


class MilitaryDetailView(generic.DetailView):
    template_name = "detail.html"
    model = Military
    context_object_name = "board"


class MilitaryUpdateView(generic.UpdateView):
    model = Military
    form_class = MilitaryModelForm
    template_name = "form.html"

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.writer != self.request.user:
            raise Http404("글을 수정할 권한이 없습니다.")
        return super(MilitaryUpdateView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy("board:mil_detail", kwargs={"pk": self.object.pk})


def military_delete(request, pk):
    board = get_object_or_404(Military, id=pk)
    if board.writer == request.user:
        board.delete()
        return redirect("/")
    else:
        raise Http404("글을 삭제할 권한이 없습니다.")


def comment_create(request):
    board = get_object_or_404(Military, pk=request.POST.get("pk"))
    if request.user.is_authenticated:
        board.score += 4
        board.save()
        if request.POST.get("Pid"):
            p = Comment.objects.get(pk=request.POST.get("Pid"))
            cmt = Comment.objects.create(
                board=board,
                content=request.POST.get("content"),
                writer=request.user,
                parents_id=p.id,
            )
            cmt.save()
            data = {
                "content": request.POST.get("content"),
                "date_str": cmt.date_str,
                "cmt_id": cmt.id,
                "cmt_count": board.comment_set.count(),
                "recmt_count": p.recomment.count(),
            }
        else:
            cmt = Comment.objects.create(
                board=board,
                content=request.POST.get("content"),
                writer=request.user,
            )
            cmt.save()
            data = {
                "content": request.POST.get("content"),
                "date_str": cmt.date_str,
                "cmt_id": cmt.id,
                "cmt_count": board.comment_set.count(),
            }
        return JsonResponse(data)
    else:
        data = {"msg": "notlogin"}
        return JsonResponse(data)


def comment_update(request):
    cmt = Comment.objects.get(pk=request.POST.get("cmt_id"))
    if request.user == cmt.writer:
        cmt.content = request.POST.get("edit_cmt")
        cmt.save()
        data = {"content": cmt.content}
        return JsonResponse(data)
    else:
        data = {"msg": "no"}
        return JsonResponse(data)


def comment_delete(request):
    board = Military.objects.get(pk=request.POST.get("pk"))
    cmt = Comment.objects.get(pk=request.POST.get("cmt_id"))
    if request.user == cmt.writer:
        cmt.delete()
        if cmt.parents:
            data = {
                "cmt_count": board.comment_set.count(),
                "Pid": cmt.parents.id,
                "recmt_count": cmt.parents.recomment.count(),
            }
        else:
            data = {"cmt_count": board.comment_set.count()}
        return JsonResponse(data)
    else:
        data = {"msg": "no"}
        return JsonResponse(data)


def like(request):
    board = Military.objects.get(pk=request.POST.get("pk"))
    if request.user.is_authenticated:
        if board.likes.filter(id=request.user.id).exists():
            data = {"msg": "exists"}
            return JsonResponse(data)
        else:
            board.like += 1
            board.score += 20
            board.likes.add(request.user)
            board.save()
            data = {"like": board.like}
            return JsonResponse(data)
    else:
        data = {"msg": "notlogin"}
        return JsonResponse(data)


def image(request):
    f2 = request.FILES.get("file")
    image = Image(image=f2)
    image.save()
    data = {"url": image.image.url}
    return JsonResponse(data)
