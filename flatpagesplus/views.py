from flatpagesplus.models import MainFlatPage, SubFlatPage
from django.template import loader, RequestContext
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.conf import settings
from django.core.xheaders import populate_xheaders
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect
from django.contrib.sites.models import get_current_site

DEFAULT_TEMPLATE = 'flatpagesplus/default.html'

# This view is called from FlatpageFallbackMiddleware.process_response
# when a 404 is raised, which often means CsrfViewMiddleware.process_view
# has not been called even if CsrfViewMiddleware is installed. So we need
# to use @csrf_protect, in case the template needs {% csrf_token %}.
# However, we can't just wrap this view; if no matching flatpage exists,
# or a redirect is required for authentication, the 404 needs to be returned
# without any CSRF checks. Therefore, we only
# CSRF protect the internal implementation.
def flatpage(request, url):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or `flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """
    if not url.startswith('/'):
        url = "/" + url
    if not url.endswith('/') and settings.APPEND_SLASH:
        return HttpResponseRedirect("%s/" % request.path)
    site = get_current_site(request)
    try:
        f = MainFlatPage.objects.get(url__exact=url, sites=site)
    except MainFlatPage.DoesNotExist:
        if url.endswith('css/'):
            p = get_object_or_404(MainFlatPage, url__exact=url[:-4], sites=site)
            try:
                return HttpResponse(p.subflatpage_set.get(type='css').content, content_type='text/css')
            except SubFlatPage.DoesNotExist:
                raise Http404
        elif url.endswith('js/'):
            p = get_object_or_404(MainFlatPage, url__exact=url[:-3], sites=site)
            try:
                return HttpResponse(p.subflatpage_set.get(type='js').content, content_type='text/javascript')
            except SubFlatPage.DoesNotExist:
                raise Http404
        else:
            raise Http404
    return render_flatpage(request, f)

@csrf_protect
def render_flatpage(request, f):
    """
    Internal interface to the flat page view.
    """
    # If registration is required for accessing this page, and the user isn't
    # logged in, redirect to the login page.
    if f.registration_required and not request.user.is_authenticated():
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(request.path)
    if f.template_name:
        t = loader.select_template((f.template_name, DEFAULT_TEMPLATE))
    else:
        t = loader.get_template(DEFAULT_TEMPLATE)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    c = RequestContext(request, {
        'flatpage': f,
    })
    response = HttpResponse(t.render(c))
    populate_xheaders(request, response, MainFlatPage, f.id)
    return response
