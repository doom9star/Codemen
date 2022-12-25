from django.shortcuts import redirect
class RedirectIfLoggedInMixin:
    def dispatch(self, req, *args, **kwargs):
        if req.user.is_authenticated:
            return redirect('home')
        return super().dispatch(req, *args, **kwargs)

class RedirectIfNotLoggedInMixin:
    def dispatch(self, req, *args, **kwargs):
        if not req.user.is_authenticated:
            return redirect('login')
        return super().dispatch(req, *args, **kwargs)
