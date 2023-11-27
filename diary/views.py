from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.urls import reverse_lazy
from .forms import DayCreateForm, ContactForm
from .models import Day
from django.views.generic import FormView
from django.contrib import messages
from django.core.mail import EmailMessage
from django.views import View

class IndexView(generic.ListView):
    model = Day
    paginate_by = 3
    template_name = 'diary/day_list.html'  # 追加

class AddView(generic.CreateView):
    model = Day
    form_class = DayCreateForm
    success_url = reverse_lazy('diary:index')
    template_name = 'diary/day_form.html'  # 追加

class UpdateView(generic.UpdateView):
    model = Day
    form_class = DayCreateForm
    success_url = reverse_lazy('diary:index')
    template_name = 'diary/day_form.html'  # 追加

class DeleteView(generic.DeleteView):
    model = Day
    success_url = reverse_lazy('diary:index')
    template_name = 'diary/day_confirm_delete.html'  # 追加

class DetailView(generic.DetailView):  # 修正
    model = Day
    template_name = 'diary/day_detail.html'  # 追加

def index(request):
    context = {
        'day_list': Day.objects.all(),
    }
    return render(request, 'diary/day_list.html', context)

def add(request):
    if request.method == 'POST':
        form = DayCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('diary:index')
    else:
        form = DayCreateForm()

    context = {
        'form': form,
    }
    return render(request, 'diary/day_form.html', context)

def update(request, pk):
    day = get_object_or_404(Day, pk=pk)
    form = DayCreateForm(request.POST or None, instance=day)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('diary:index')

    context = {
        'form': form
    }
    return render(request, 'diary/day_form.html', context)

def delete(request, pk):
    day = get_object_or_404(Day, pk=pk)
    if request.method == 'POST':
        day.delete()
        return redirect('diary:index')

    context = {
        'day': day
    }
    return render(request, 'diary/day_confirm_delete.html', context)

class ContactView(FormView):
    template_name = 'diary/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('diary:contact_after')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        subject = '感想: {}'.format(title)
        message_text = '送信者名: {0}\nメールアドレス: {1}\n タイトル:{2}\n メッセージ:\n{3}'.format(
            name, email, title, message)

        from_email = 'admin@example.com'
        to_list = ['admin@example.com']
        message = EmailMessage(
            subject=subject, body=message_text, from_email=from_email, to=to_list)

        message.send()

        # リダイレクト処理をここで行う
        response = super().form_valid(form)

        messages.success(
            self.request, '感想は正常に送信されました.')

        return response  # レスポンスを返す
class ContactAfterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'diary/contact_after.html')
