from django import forms
from django.contrib import admin
from flatpagesplus.models import MainFlatPage, SubFlatPage
from django.utils.translation import ugettext_lazy as _


class MainFlatPageForm(forms.ModelForm):
    url = forms.RegexField(label=_("URL"), max_length=100, regex=r'^[-\w/\.~]+$',
        help_text = _("Example: '/about/contact/'. Make sure to have leading"
                      " and trailing slashes."),
        error_message = _("This value must contain only letters, numbers,"
                          " dots, underscores, dashes, slashes or tildes."))

    class Meta:
        model = MainFlatPage


class SubFlatPageInline(admin.StackedInline):
    model = SubFlatPage
    extra = 2
    max_num = 2
    verbose_name = 'linked media'


class MainFlatPageAdmin(admin.ModelAdmin):
    form = MainFlatPageForm
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content', 'sites')}),
        (_('Advanced options'), {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name', 'embedded_head_content', 'embedded_foot_content')}),
    )
    list_display = ('url', 'title')
    list_filter = ('sites', 'enable_comments', 'registration_required')
    search_fields = ('url', 'title')
    inlines = [
        SubFlatPageInline,
    ]

admin.site.register(MainFlatPage, MainFlatPageAdmin)
