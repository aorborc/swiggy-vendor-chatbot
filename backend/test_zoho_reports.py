import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from tools.zoho_service import ZohoAnalyticsService


class TestZohoReports(unittest.TestCase):
    def setUp(self):
        self.service = ZohoAnalyticsService()
        self.temp_dir = Path(tempfile.mkdtemp())
        self.service.export_dir = self.temp_dir
        self.service.client = MagicMock()
        self.service.client.workspace_id = "TEST_WORKSPACE"
        self.service.client.is_configured.return_value = True

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_fetch_invoice_dashboard_report(self):
        slug = "invoice_dashboard_2"
        expected_path = str(self.temp_dir / f"{slug}.json")

        self.service.fetch_report(slug, "TEST_PAN")

        self.service.client.call_tool.assert_called_with(
            "export_view",
            {
                "workspace_id": "TEST_WORKSPACE",
                "view_id": "234338000007714196",
                "criteria": "\"Invoice  Query Table\".\"PAN Number\" = 'TEST_PAN'",
                "response_file_format": "json",
                "response_file_path": expected_path,
            },
        )

    def test_default_pan_is_used(self):
        slug = "ar_invoice_report_2"
        expected_path = str(self.temp_dir / f"{slug}.json")

        self.service.fetch_report(slug)

        self.service.client.call_tool.assert_called_with(
            "export_view",
            {
                "workspace_id": "TEST_WORKSPACE",
                "view_id": "234338000007665998",
                "criteria": "\"AR Invoice - Query Table\".\"PAN\" = 'AAMCA0969R'",
                "response_file_format": "json",
                "response_file_path": expected_path,
            },
        )

    def test_all_reports_loaded_from_csv(self):
        self.assertGreaterEqual(len(self.service.available_reports), 13)
        self.assertIn("za_monthly_summary", self.service.available_reports)
        self.assertIn("collection_adjustment_at_ar_invoice_level", self.service.available_reports)


if __name__ == "__main__":
    unittest.main()
