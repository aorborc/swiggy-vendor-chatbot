from typing import Any, Callable, Dict, List, Optional

from tools.zoho_service import ReportConfig, zoho_service

tools_list: List[Callable[..., List[Dict[str, Any]]]] = []


def _build_tool(slug: str, config: ReportConfig) -> Callable[[Optional[str]], List[Dict[str, Any]]]:
    def _tool(pan: Optional[str] = None) -> List[Dict[str, Any]]:
        return zoho_service.fetch_report(slug, pan) or []

    _tool.__name__ = f"get_{slug}"
    _tool.__doc__ = f"Retrieve '{config.title}' data (View ID: {config.view_id})."
    return _tool


for slug, config in zoho_service.available_reports.items():
    tool_fn = _build_tool(slug, config)
    globals()[tool_fn.__name__] = tool_fn
    tools_list.append(tool_fn)
