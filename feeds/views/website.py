import logging

from django import forms
from django.views.generic import ListView, DetailView
from django.views.generic import CreateView, UpdateView
from django.views.generic import DeleteView
from django.utils.translation import ugettext as _
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin


from ..mixins import PaginateListMixin
from ..models import WebSite, Feed
from ..forms import WebSiteCreateForm, WebSiteFeedAddForm
from ..forms import WebSiteUpdateForm, FeedAddForm
from ..tools import getFeedsFromSite

from formtools.wizard.views import SessionWizardView


WebSiteSubmitForms = [
    ('WebSite', WebSiteCreateForm),
    ('Feeds', WebSiteFeedAddForm),
    ]


logger = logging.getLogger(__name__)

class WebSiteSubmitWizardView(LoginRequiredMixin, SessionWizardView):
    """
    Wizard that walks people through when adding a site with feeds
    """
    template_name = "feeds/website_submit_wizard.html"
    form_list = [WebSiteCreateForm, WebSiteFeedAddForm]

    def get_form(self, step=None, data=None, files=None):
        form = super(WebSiteSubmitWizardView, self).get_form(step, data, files)

        step = step or self.steps.current

        if step == u'Feeds':
            # form = WebSiteFeedAddForm()
            step_0_data = self.storage.get_step_data('WebSite')
            links = getFeedsFromSite(step_0_data['WebSite-url'])
            for title, href in links:
                form.fields[href] = forms.BooleanField(
                    initial=False,
                    required=False,
                    label=title
                )
        return form

    def done(self, form_list, form_dict, **kwargs):
        from django.contrib import messages
        site_form = form_dict['WebSite']
        feed_form = form_dict['Feeds']
        if site_form.is_valid() and feed_form.is_valid():
            site = WebSite(url=site_form.url).save()
            for feed in feed_form.fields:
                f = Feed.get_or_create(
                    website=site,
                    feed_url=feed.url,
                    name=feed.name
                )
                f.save()

            messages.add_message(
                self.request,
                messages.INFO,
                _("Successfully submitted site.")
                )
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                _("Error submitted site.")
            )
        return HttpResponseRedirect(reverse('planet:website-home'))


class WebSiteListView(LoginRequiredMixin, PaginateListMixin, ListView):
    """
    Lists all sites in the database.

    The view is accessible publically.

    :url: planet:site-home

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """

    model = WebSite
    template_name = "feeds/website_list.html"

    def get_queryset(self):
        return WebSite.objects.order_by('netloc')


class WebSiteCreateView(PermissionRequiredMixin, CreateView):
    """
    View to create a new site.
    """
    permission_required = "feeds.add_site"
    form_class = WebSiteCreateForm
    model = WebSite


class WebSiteDetailView(DetailView):
    """
    Shows Details for one particular :py:mod:`feeds.models.WebSite`.

    The view is accessible publically.

    :url: planet:site-detail

    .. codeauthor:: Andreas Neumeier <andreas@neumeier.org>
    """
    model = WebSite
    template_name = "feeds/website_detail.html"

    def get_context_data(self, **kwargs):
        context = super(WebSiteDetailView, self).get_context_data(**kwargs)
        all_feeds = getFeedsFromSite(self.object.website_url)
        existing = [feed.feed_url for feed in Feed.objects.filter(
                        feed_url__in=all_feeds).filter(
                        website=self.object.pk
                        )
                    ]
        context['new_feeds'] = []
        for f in (set(all_feeds) - set(existing)):
            form = \
                FeedAddForm(
                    instance=Feed(
                        website=self.object,
                        feed_url=f
                        )
                        )

            context['new_feeds'].append(form)

        context['existing'] = Feed.objects.filter(feed_url__in=existing)
        return context


class WebSiteUpdateView(PermissionRequiredMixin, UpdateView):
    """
    Update WebSite.

    Update an existing `WebSite`.
    """

    permission_required = "feeds.change_site"
    form_class = WebSiteUpdateForm
    model = WebSite


class WebSiteDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "feeds.delete_site"
    model = WebSite
    success_url = "planet:site-home"
