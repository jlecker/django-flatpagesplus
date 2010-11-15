from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site
from django.utils.translation import ugettext_lazy as _


class MainFlatPage(models.Model):
    """A page to be viewed (HTML format, etc)."""
    url = models.CharField(_('URL'), max_length=100, db_index=True)
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    embedded_head_content = models.TextField(_('head content'), blank=True)
    embedded_foot_content = models.TextField(_('foot content'), blank=True)
    enable_comments = models.BooleanField(_('enable comments'))
    template_name = models.CharField(_('template name'), max_length=70, blank=True,
        help_text=_("Example: 'flatpagesplus/contact_page.html'. If this isn't provided, the system will use 'flatpagesplus/default.html'."))
    registration_required = models.BooleanField(_('registration required'), help_text=_("If this is checked, only logged-in users will be able to view the page."))
    sites = models.ManyToManyField(Site)

    class Meta:
        verbose_name = _('main flat page')
        verbose_name_plural = _('main flat pages')
        ordering = ('url',)

    def __unicode__(self):
        return u'%s -- %s' % (self.url, self.title)

    def get_absolute_url(self):
        return self.url
    
    @property
    def head_content(self):
        content_list = []
        if self.embedded_head_content:
            content_list.append(self.embedded_head_content)
        if SubFlatPage.objects.filter(parent=self, type='css', insert_link=True).exists():
            content_list.append('<link rel="stylesheet" type="text/css" href="css/" media="screen, projection" />')
        return mark_safe('\n'.join(content_list))
    
    @property
    def foot_content(self):
        content_list = []
        if self.embedded_foot_content:
            content_list.append(self.embedded_foot_content)
        if SubFlatPage.objects.filter(parent=self, type='js', insert_link=True).exists():
            content_list.append('<script type="text/javascript" src="js/"></script>')
        return mark_safe('\n'.join(content_list))


SUB_TYPE_CHOICES = (
    ('css', 'cascading style sheet'),
    ('js', 'JavaScript source'),
)

class SubFlatPage(models.Model):
    """
    A page linked to by a MainFlatPage, not be viewed directly (CSS, JS, etc.).
    
    """
    
    parent = models.ForeignKey(MainFlatPage, verbose_name=_('parent page'))
    type = models.CharField(_('subpage type'), max_length=3, choices=SUB_TYPE_CHOICES)
    content = models.TextField(_('content'))
    insert_link = models.BooleanField(_('insert link'), default=True,
        help_text=_('Automatically insert a link or script tag for this subpage into the parent page?'))
    
    class Meta:
        verbose_name = _('sub flat page')
        verbose_name_plural = _('sub flat pages')
        unique_together = ('parent', 'type')
    
    def __unicode__(self):
        return u'%s for %s' % (self.type, self.parent)
