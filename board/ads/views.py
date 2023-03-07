from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import Post, Category, PostCategory, Reply
from .forms import PostForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.shortcuts import redirect, get_object_or_404, render
from .tasks import mail_new

class AdsList(ListView):
    model = Post
    ordering = '-time_in'
    template_name = 'flatpages/ads.html'
    context_object_name = 'ads'
    paginate_by = 2

class AdsDetail(DetailView):
    model = Post
    template_name = 'flatpages/ad.html'
    context_object_name = 'ad'

class AdsCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/ads_edit.html'

    def form_valid(self, form):
        mail_new.apply_async(countdown=5)

class ReplyCreate(LoginRequiredMixin, CreateView):
    form_class = ReplyForm
    model = Reply
    template_name = 'flatpages/reply_edit.html'

    def get_success_url(self):
        return redirect('/ads/')



#    def form_valid(self, form):
#        reply = form.save(commit=False)
#        reply.post = Post.objects.get(id=pk)
#        return super().form_valid(form)


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

@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = 'Вы подписались на рассылку объявлений данной категории'
    return render(request, 'ads/subscribe.html', {'category': category, 'message': message})
