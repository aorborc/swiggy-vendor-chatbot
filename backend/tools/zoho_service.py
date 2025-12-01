from __future__ import annotations

import csv
import json
import os
import re
import tempfile
from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Any, List, Mapping, Optional

from .mcp_client import zoho_mcp_client


@dataclass(frozen=True)
class ReportConfig:
    """Represents a Zoho Analytics view that can be exported via MCP."""

    title: str
    slug: str
    view_id: str
    criteria_template: str
    report_number: int
    portal_page_url: Optional[str] = None
    admin_page_url: Optional[str] = None


class ZohoAnalyticsService:
    """
    Service that maps every report in VendorPortalReportsList.csv to an MCP tool call.
    Each report uses the export_view tool with a PAN-aware criteria expression.
    """

    REPORTS_CSV = Path(__file__).resolve().parents[2] / "VendorPortalReportsList.csv"

    def __init__(self) -> None:
        self.client = zoho_mcp_client
        self.demo_pan = os.getenv("DEFAULT_VENDOR_PAN", "AAMCA0969R")
        self.export_dir = Path(os.getenv("ZOHO_EXPORT_DIR", tempfile.gettempdir()))
        self.export_dir.mkdir(parents=True, exist_ok=True)
        self._reports: "OrderedDict[str, ReportConfig]" = self._load_reports_from_csv()

    @property
    def available_reports(self) -> Mapping[str, ReportConfig]:
        """Expose the ordered mapping of report slug -> config."""
        return self._reports

    def fetch_report(self, report_slug: str, pan: Optional[str] = None) -> Optional[List[Dict[str, Any]]]:
        """
        Fetches a report identified by slug.
        The slug is derived from the Title column (snake_case).
        """
        report = self._reports.get(report_slug)
        if not report:
            raise KeyError(f"Report '{report_slug}' was not found in VendorPortalReportsList.csv")

        if not self.client.is_configured():
            print("Zoho MCP not configured, returning None")
            return None

        vendor_pan = pan or self.demo_pan
        criteria = report.criteria_template.format(pan=vendor_pan)
        output_file = self.export_dir / f"{report_slug}.json"

        print(f"Fetching '{report.title}' for PAN {vendor_pan} (View ID: {report.view_id})")

        self.client.call_tool(
            "export_view",
            {
                "workspace_id": self.client.workspace_id,
                "view_id": report.view_id,
                "criteria": criteria,
                "response_file_format": "json",
                "response_file_path": str(output_file),
            },
        )

        if output_file.exists():
            try:
                with output_file.open("r", encoding="utf-8") as file_handle:
                    return json.load(file_handle)
            except Exception as exc:  # pragma: no cover - defensive logging
                print(f"Error reading report output for {report_slug}: {exc}")
                return None

        return None

    def _load_reports_from_csv(self) -> "OrderedDict[str, ReportConfig]":
        if not self.REPORTS_CSV.exists():
            raise FileNotFoundError(f"Unable to locate {self.REPORTS_CSV}")

        ordered_configs: "OrderedDict[str, ReportConfig]" = OrderedDict()
        rows: List[ReportConfig] = []

        with self.REPORTS_CSV.open("r", newline="", encoding="utf-8-sig") as csv_file:
            reader = csv.DictReader(csv_file)
            for index, row in enumerate(reader, start=1):
                title = (row.get("Title") or "").strip()
                view_id = (row.get("Analytics View ID") or "").strip()
                criteria = (row.get("Portal Criteria") or "").strip()

                if not title or not view_id or not criteria:
                    continue

                slug = self._slugify(title)
                criteria_template = self._normalize_criteria(criteria)
                report_number = self._parse_report_number(row.get("Report Number"), fallback=index)

                rows.append(
                    ReportConfig(
                        title=title,
                        slug=slug,
                        view_id=view_id,
                        criteria_template=criteria_template,
                        report_number=report_number,
                        portal_page_url=(row.get("Portal Page URL") or "").strip() or None,
                        admin_page_url=(row.get("Admin Page URL") or "").strip() or None,
                    )
                )

        for report in sorted(rows, key=lambda cfg: cfg.report_number):
            ordered_configs[report.slug] = report

        return ordered_configs

    def _slugify(self, value: str) -> str:
        slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
        return slug or "report"

    def _normalize_criteria(self, criteria: str) -> str:
        if "{pan}" in criteria:
            return criteria
        trimmed = criteria.strip()
        if trimmed.endswith("="):
            trimmed = trimmed[:-1].rstrip()
        return f"{trimmed} = '{{pan}}'"

    def _parse_report_number(self, raw_value: Optional[str], fallback: int) -> int:
        if not raw_value:
            return fallback
        try:
            return int(raw_value.strip())
        except ValueError:
            return fallback


zoho_service = ZohoAnalyticsService()
