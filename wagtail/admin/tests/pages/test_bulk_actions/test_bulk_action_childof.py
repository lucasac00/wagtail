from django.test import TestCase
from django.urls import reverse

from wagtail.models import Page
from wagtail.test.testapp.models import SimplePage
from wagtail.test.utils import WagtailTestUtils


class TestPageBulkActionInvalidChildOf(WagtailTestUtils, TestCase):
    """
    Regression tests for #14388.

    When a bulk action is performed with "Select all in listing"
    (``id=all&childOf=<page_id>``) and the page referenced by ``childOf`` no
    longer exists, the view must return a 404 instead of crashing with an
    unhandled ``Page.DoesNotExist`` (HTTP 500).
    """

    def setUp(self):
        self.root_page = Page.objects.get(id=2)
        self.child = SimplePage(
            title="Child", slug="child-14388", content="x", live=True
        )
        self.root_page.add_child(instance=self.child)
        self.login()

    def _url(self, child_of):
        return (
            reverse("wagtail_bulk_action", args=("wagtailcore", "page", "publish"))
            + f"?id=all&childOf={child_of}"
        )

    def test_select_all_with_nonexistent_childof_returns_404(self):
        # Antes da correção: Page.DoesNotExist (HTTP 500). Depois: 404.
        response = self.client.get(self._url(999999))
        self.assertEqual(response.status_code, 404)

    def test_select_all_with_valid_childof_still_works(self):
        # Garante que o caso válido continua funcionando (sem regressão).
        response = self.client.get(self._url(self.root_page.id))
        self.assertEqual(response.status_code, 200)
