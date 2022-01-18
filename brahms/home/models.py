from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel
from wagtail.core.models import Page
from django.db import models
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index


class HomePage(Page):
    description = models.TextField(verbose_name='description', blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel('description')],
            heading="Description",
            classname="collapsible collapsed"
        ),
        ImageChooserPanel('image')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('description'),
    ]

    class Meta:
        verbose_name = 'Home Page'
