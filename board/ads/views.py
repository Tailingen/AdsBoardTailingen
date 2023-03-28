import logging
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Author, Post, Category, PostCategory, Reply
from .forms import PostForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.shortcuts import redirect, get_object_or_404, render

class AdsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'flatpages/ads.html'
    context_object_name = 'ads'
    paginate_by = 2

class ReplyList(ListView):
    model = Reply
    ordering = '-time_in'
    template_name = 'flatpages/all_replys.html'
    context_object_name = 'all_replys'

class AdsDetail(DetailView):
    model = Post
    template_name = 'flatpages/ad.html'
    context_object_name = 'ad'

class AdsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/ads_edit.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.get(user=self.request.user)
        return super().form_valid(form)

class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'flatpages/reply_edit.html'

    def form_valid(self, form):
        reply = form.save(commit=False)
        reply.user = Author.objects.get(user=self.request.user)
        send_mail(
                    subject=f'Новый отклик {Reply.post}',
                    message='У вашего объявления новый отклик',
                    from_email='Tailingen1@yandex.ru',
                    recipient_list=['Tailingen@mail.ru']
                )
#        reply.post = Post.objects.get(pk=self.request.GET.get('post_pk'))
        return super().form_valid(form)


class ReplyDelete(LoginRequiredMixin, DeleteView):
    model = Reply
    template_name = 'flatpages/reply_delete.html'
    success_url = reverse_lazy('post_list')


class AdsUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/ads_edit.html'

class AdsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'flatpages/ads_delete.html'
    success_url = reverse_lazy('post_list')

class CategoryListView(ListView):
    model = Post
    template_name = 'ads/category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(category=self.category).order_by("-time_in")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

class ReplyDetail(DetailView):
    model = Reply
    template_name = 'flatpages/replys.html'
    context_object_name = 'replys'

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку объявлений данной категории'
    return render(request, 'ads/subscribe.html', {'category': category, 'message': message})

def notifi_reply(request, pk):
    user = request.user
    reply = Reply.objects.get(id=pk)
    send_mail(
        subject=f'Одобрение отклика {Reply.post}',
        message='Автор объявления одобрил ваш отклик',
        from_email='Tailingen1@yandex.ru',
        recipient_list=[user.email]
    )
    message = 'Отклик одобрен'
    return render(request, 'ads/notifi.html', {'reply': reply, 'message': message})
