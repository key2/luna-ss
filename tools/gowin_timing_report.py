#!/usr/bin/env python3
"""Extract and display timing reports from Gowin IDE HTML output.

Gowin IDE (used by the Amaranth HDL ``GowinPlatform`` backend) generates
several HTML report files after place-and-route.  These files are deeply
nested HTML tables with inconsistent markup (missing closing tags, inline
styles for carry-chain highlighting, etc.) that are difficult to read in
a browser during iterative FPGA development.

This tool parses every report file produced by a Gowin PnR run and
extracts the data into structured Python objects, then renders a concise
terminal summary.  It can also dump the full parsed data as JSON for
downstream tooling or CI/CD integration.

Supported report files
----------------------
All files are found under ``<build_dir>/impl/``:

=================================  ==================================================
File                               Content
=================================  ==================================================
``pnr/project_tr_content.html``    **Timing analysis** — clocks, Fmax, TNS, setup /
                                   hold slack tables, detailed paths with arrival and
                                   required path breakdowns, min pulse width, high
                                   fanout nets, route congestion, SDC constraints.
``pnr/project.rpt.html``          **PnR report** — resource usage, I/O banks, global
                                   clocks, pin assignments.
``pnr/project.power.html``        **Power analysis** — total / quiescent / dynamic
                                   power, thermal info, supply currents, per-block
                                   and per-hierarchy power breakdown.
``gwsynthesis/project_syn.rpt.html``  **Synthesis report** — resource usage, clock
                                   summary, Fmax, and detailed timing paths (pre-PnR).
=================================  ==================================================

Architecture
------------
The parser uses Python's ``html.parser.HTMLParser`` (stdlib, no external
dependencies) to build a lightweight DOM from the malformed Gowin HTML.
Each report section is identified by its ``<a name="...">`` anchor inside
heading tags (``<h1>``, ``<h2>``, ``<h3>``).  Tables are classified by
their CSS class:

- ``summary_table`` — key-value pairs (label in ``td.label``, value in
  next ``<td>``).
- ``detail_table`` — multi-column data tables with ``<th>`` headers.
- Unclassed ``<table>`` — treated as detail tables (e.g. Max Frequency).

The parser tolerates missing ``</td>`` and ``</tr>`` tags that Gowin's
power and resource reports emit.

Usage
-----
**Terminal summary** (default)::

    python gowin_timing_report.py build/

**JSON output** for machine consumption::

    python gowin_timing_report.py build/ --json

**Filter to specific sections**::

    python gowin_timing_report.py build/ --section fmax --section resources

**Show worst N timing paths**::

    python gowin_timing_report.py build/ --paths 5

Available ``--section`` filters:
  ``meta``, ``clocks``, ``fmax``, ``tns``, ``setup-slack``,
  ``hold-slack``, ``min-pulse-width``, ``resources``, ``io-banks``,
  ``global-clocks``, ``pins``, ``power``, ``thermal``, ``supply``,
  ``high-fanout``, ``congestion``, ``sdc``, ``paths``

If no ``--section`` is given, the summary prints all sections.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Lightweight DOM builder — tolerant of Gowin's malformed HTML
# ---------------------------------------------------------------------------


class _Node:
    """Minimal DOM node for HTML table extraction."""

    __slots__ = ("tag", "attrs", "children", "text", "parent")

    def __init__(self, tag: str, attrs: dict[str, str]):
        self.tag = tag
        self.attrs = attrs
        self.children: list[_Node] = []
        self.text = ""
        self.parent: _Node | None = None

    def find_all(self, tag: str, **attr_filters) -> list[_Node]:
        """Depth-first search for nodes matching *tag* and attribute filters."""
        results: list[_Node] = []
        stack = list(self.children)
        while stack:
            node = stack.pop(0)
            if node.tag == tag:
                if all(node.attrs.get(k) == v for k, v in attr_filters.items()):
                    results.append(node)
            stack = list(node.children) + stack
        return results

    def find(self, tag: str, **attr_filters) -> _Node | None:
        hits = self.find_all(tag, **attr_filters)
        return hits[0] if hits else None

    def get_text(self) -> str:
        """Recursively collect all text content, stripping whitespace."""
        parts = [self.text]
        for child in self.children:
            parts.append(child.get_text())
        return " ".join(parts).strip()

    def __repr__(self):
        return f"<{self.tag} {self.attrs}>"


class _DOMBuilder(HTMLParser):
    """Build a minimal DOM tree from Gowin IDE HTML."""

    # Tags that Gowin sometimes leaves unclosed
    _SELF_CLOSING = frozenset(("br", "hr", "img", "input", "meta", "link"))
    _AUTO_CLOSE = frozenset(("td", "th", "tr", "li", "p"))

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = _Node("root", {})
        self._current = self.root
        self._stack: list[_Node] = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag = tag.lower()
        # Auto-close unclosed peer tags (Gowin omits </td>, </tr>, etc.)
        if tag in self._AUTO_CLOSE:
            while self._current.tag == tag:
                self._pop()

        attr_dict = {k: (v or "") for k, v in attrs}
        node = _Node(tag, attr_dict)
        node.parent = self._current
        self._current.children.append(node)

        if tag not in self._SELF_CLOSING:
            self._stack.append(node)
            self._current = node

    def handle_endtag(self, tag: str):
        tag = tag.lower()
        # Walk up the stack to find the matching open tag
        for i in range(len(self._stack) - 1, 0, -1):
            if self._stack[i].tag == tag:
                while len(self._stack) > i:
                    self._pop()
                return

    def handle_data(self, data: str):
        cleaned = data.replace("\xa0", " ").strip()
        if cleaned:
            self._current.text += (" " + cleaned) if self._current.text else cleaned

    def _pop(self):
        if len(self._stack) > 1:
            self._stack.pop()
            self._current = self._stack[-1]


def _parse_html(html_text: str) -> _Node:
    """Parse HTML string into a lightweight DOM tree."""
    builder = _DOMBuilder()
    builder.feed(html_text)
    return builder.root


# ---------------------------------------------------------------------------
# Table extraction helpers
# ---------------------------------------------------------------------------


def _extract_rows(table_node: _Node) -> list[list[str]]:
    """Extract all rows from a <table> node as lists of cell text."""
    rows: list[list[str]] = []
    for tr in table_node.find_all("tr"):
        cells: list[str] = []
        for child in tr.children:
            if child.tag in ("td", "th"):
                cells.append(child.get_text())
        if cells:
            rows.append(cells)
    return rows


def _extract_kv_table(table_node: _Node) -> dict[str, str]:
    """Extract a key-value table (summary_table pattern)."""
    kv: dict[str, str] = {}
    for row in _extract_rows(table_node):
        if len(row) >= 2:
            kv[row[0].strip()] = row[1].strip()
    return kv


def _extract_detail_table(table_node: _Node) -> list[dict[str, str]]:
    """Extract a multi-column table into a list of dicts keyed by header."""
    rows = _extract_rows(table_node)
    if not rows:
        return []

    # First row with <th> cells is the header
    header_row: list[str] | None = None
    data_rows: list[list[str]] = []
    for tr in table_node.find_all("tr"):
        cells = [c for c in tr.children if c.tag in ("td", "th")]
        if not cells:
            continue
        if any(c.tag == "th" for c in cells):
            header_row = [c.get_text().strip() for c in cells]
        else:
            data_rows.append([c.get_text().strip() for c in cells])

    if header_row is None:
        # No headers found — return raw rows
        return [{"col_" + str(i): v for i, v in enumerate(row)} for row in rows]

    result: list[dict[str, str]] = []
    for row in data_rows:
        entry = {}
        for i, hdr in enumerate(header_row):
            entry[hdr] = row[i] if i < len(row) else ""
        result.append(entry)
    return result


# ---------------------------------------------------------------------------
# Section anchor discovery
# ---------------------------------------------------------------------------


def _find_sections(root: _Node) -> dict[str, _Node]:
    """Map anchor names to their parent heading nodes.

    Gowin uses ``<h1><a name="Section">Title</a></h1>`` etc.
    """
    anchors: dict[str, _Node] = {}
    for a_node in root.find_all("a"):
        name = a_node.attrs.get("name", "")
        if name:
            anchors[name] = a_node.parent or a_node
    return anchors


def _tables_after_anchor(root: _Node, anchor_name: str) -> list[_Node]:
    """Find all <table> elements that follow a given anchor in document order.

    Stops collecting when the next heading with an ``<a name="...">``
    anchor is encountered — this marks the start of a new report section.
    The heading that *contains* the searched anchor is already behind the
    anchor position in DFS order, so it is never revisited.
    """
    # Flatten to document order
    flat: list[_Node] = []
    stack = [root]
    while stack:
        node = stack.pop(0)
        flat.append(node)
        stack = list(node.children) + stack

    # Find the anchor position
    anchor_idx = None
    for i, node in enumerate(flat):
        if node.tag == "a" and node.attrs.get("name") == anchor_name:
            anchor_idx = i
            break

    if anchor_idx is None:
        return []

    # Collect tables until the next heading that starts a new section.
    # A "new section" heading is any <h1>/<h2>/<h3> that contains an
    # <a name="..."> anchor different from the one we searched for.
    tables: list[_Node] = []
    heading_tags = {"h1", "h2", "h3"}
    for node in flat[anchor_idx + 1 :]:
        if node.tag in heading_tags:
            has_new_anchor = any(
                c.tag == "a"
                and c.attrs.get("name")
                and c.attrs.get("name") != anchor_name
                for c in node.children
            )
            if has_new_anchor:
                break
        if node.tag == "table":
            tables.append(node)

    return tables


# ---------------------------------------------------------------------------
# Dataclasses for structured report data
# ---------------------------------------------------------------------------


@dataclass
class ClockInfo:
    name: str
    type: str
    period_ns: float
    frequency_mhz: float
    rise: float
    fall: float
    source: str
    master: str
    objects: str


@dataclass
class FmaxInfo:
    clock_name: str
    constraint_mhz: float
    actual_fmax_mhz: float
    logic_level: int
    entity: str
    met: bool  # True if actual >= constraint


@dataclass
class SlackEntry:
    path_number: int
    slack_ns: float
    from_node: str
    to_node: str
    from_clock: str
    to_clock: str
    relation_ns: float
    clock_skew_ns: float
    data_delay_ns: float


@dataclass
class TNSEntry:
    clock_name: str
    analysis_type: str
    endpoints_tns: float
    num_endpoints: int


@dataclass
class MinPulseWidth:
    number: int
    slack_ns: float
    actual_width_ns: float
    required_width_ns: float
    type: str
    clock: str
    objects: str


@dataclass
class TimingPathSummary:
    slack_ns: float
    data_arrival_time_ns: float
    data_required_time_ns: float
    from_node: str
    to_node: str
    launch_clk: str
    latch_clk: str


@dataclass
class TimingPathStep:
    at_ns: float
    delay_ns: float
    type: str
    rf: str
    fanout: str
    loc: str
    node: str


@dataclass
class TimingPathStats:
    clock_skew_ns: float
    setup_relationship_ns: float
    logic_level: int
    arrival_clock_path: str
    arrival_data_path: str
    required_clock_path: str


@dataclass
class DetailedTimingPath:
    analysis_type: str  # "Setup" or "Hold"
    path_number: int
    summary: TimingPathSummary
    arrival_path: list[TimingPathStep]
    required_path: list[TimingPathStep]
    statistics: TimingPathStats | None


@dataclass
class ResourceUsage:
    resource: str
    usage: str
    utilization: str


@dataclass
class HighFanoutNet:
    fanout: int
    net_name: str
    worst_slack_ns: float
    max_delay_ns: float


@dataclass
class RouteCongestion:
    grid_loc: str
    congestion_pct: float


@dataclass
class SDCConstraint:
    command_type: str
    state: str
    detail_command: str


@dataclass
class PowerInfo:
    total_mw: float
    quiescent_mw: float
    dynamic_mw: float


@dataclass
class ThermalInfo:
    junction_temp_c: float
    theta_ja: float
    max_ambient_temp_c: float


@dataclass
class SupplyInfo:
    source: str
    voltage_v: float
    dynamic_current_ma: float
    quiescent_current_ma: float
    power_mw: float


@dataclass
class GowinTimingReport:
    """Complete parsed Gowin IDE report data."""

    # Metadata
    metadata: dict[str, str] = field(default_factory=dict)
    # Timing summaries
    sta_summary: dict[str, str] = field(default_factory=dict)
    clocks: list[ClockInfo] = field(default_factory=list)
    fmax: list[FmaxInfo] = field(default_factory=list)
    tns: list[TNSEntry] = field(default_factory=list)
    # Slack tables
    setup_slack: list[SlackEntry] = field(default_factory=list)
    hold_slack: list[SlackEntry] = field(default_factory=list)
    min_pulse_width: list[MinPulseWidth] = field(default_factory=list)
    # Detailed paths
    detailed_paths: list[DetailedTimingPath] = field(default_factory=list)
    # Resource usage (from PnR report)
    resources: list[ResourceUsage] = field(default_factory=list)
    io_banks: list[dict[str, str]] = field(default_factory=list)
    global_clocks: list[dict[str, str]] = field(default_factory=list)
    pins: list[dict[str, str]] = field(default_factory=list)
    # High fanout / congestion
    high_fanout: list[HighFanoutNet] = field(default_factory=list)
    route_congestion: list[RouteCongestion] = field(default_factory=list)
    sdc_constraints: list[SDCConstraint] = field(default_factory=list)
    # Power (from power report)
    power: PowerInfo | None = None
    thermal: ThermalInfo | None = None
    supply: list[SupplyInfo] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Parsing functions for each report file
# ---------------------------------------------------------------------------


def _safe_float(s: str, default: float = 0.0) -> float:
    try:
        return float(s.strip())
    except (ValueError, AttributeError):
        return default


def _safe_int(s: str, default: int = 0) -> int:
    try:
        return int(s.strip())
    except (ValueError, AttributeError):
        return default


def _parse_fmax_value(s: str) -> float:
    """Parse '371.229(MHz)' → 371.229."""
    m = re.match(r"([\d.]+)", s)
    return float(m.group(1)) if m else 0.0


def _parse_slack_rows(rows: list[dict[str, str]]) -> list[SlackEntry]:
    entries: list[SlackEntry] = []
    for row in rows:
        entries.append(
            SlackEntry(
                path_number=_safe_int(row.get("Path Number", "0")),
                slack_ns=_safe_float(row.get("Path Slack", "0")),
                from_node=row.get("From Node", ""),
                to_node=row.get("To Node", ""),
                from_clock=row.get("From Clock", ""),
                to_clock=row.get("To Clock", ""),
                relation_ns=_safe_float(row.get("Relation", "0")),
                clock_skew_ns=_safe_float(row.get("Clock Skew", "0")),
                data_delay_ns=_safe_float(row.get("Data Delay", "0")),
            )
        )
    return entries


def parse_timing_report(html_text: str, report: GowinTimingReport) -> None:
    """Parse project_tr_content.html into the report object."""
    root = _parse_html(html_text)

    # --- Metadata ---
    tables = _tables_after_anchor(root, "Message")
    if tables:
        report.metadata.update(_extract_kv_table(tables[0]))

    # --- STA Tool Run Summary ---
    tables = _tables_after_anchor(root, "STA_Tool_Run_Summary")
    if tables:
        report.sta_summary = _extract_kv_table(tables[0])

    # --- Clock Report ---
    tables = _tables_after_anchor(root, "Clock_Report")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            report.clocks.append(
                ClockInfo(
                    name=row.get("Clock Name", ""),
                    type=row.get("Type", ""),
                    period_ns=_safe_float(row.get("Period", "0")),
                    frequency_mhz=_safe_float(row.get("Frequency(MHz)", "0")),
                    rise=_safe_float(row.get("Rise", "0")),
                    fall=_safe_float(row.get("Fall", "0")),
                    source=row.get("Source", ""),
                    master=row.get("Master", ""),
                    objects=row.get("Objects", ""),
                )
            )

    # --- Max Frequency Report ---
    tables = _tables_after_anchor(root, "Max_Frequency_Report")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            constraint = _parse_fmax_value(row.get("Constraint", "0"))
            actual = _parse_fmax_value(row.get("Actual Fmax", "0"))
            report.fmax.append(
                FmaxInfo(
                    clock_name=row.get("Clock Name", ""),
                    constraint_mhz=constraint,
                    actual_fmax_mhz=actual,
                    logic_level=_safe_int(row.get("Logic Level", "0")),
                    entity=row.get("Entity", ""),
                    met=actual >= constraint,
                )
            )

    # --- TNS Report ---
    tables = _tables_after_anchor(root, "Total_Negative_Slack_Report")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            report.tns.append(
                TNSEntry(
                    clock_name=row.get("Clock Name", ""),
                    analysis_type=row.get("Analysis Type", ""),
                    endpoints_tns=_safe_float(row.get("Endpoints TNS", "0")),
                    num_endpoints=_safe_int(row.get("Number of Endpoints", "0")),
                )
            )

    # --- Setup Slack Table ---
    tables = _tables_after_anchor(root, "Setup_Slack_Table")
    for tbl in tables:
        report.setup_slack.extend(_parse_slack_rows(_extract_detail_table(tbl)))

    # --- Hold Slack Table ---
    tables = _tables_after_anchor(root, "Hold_Slack_Table")
    for tbl in tables:
        report.hold_slack.extend(_parse_slack_rows(_extract_detail_table(tbl)))

    # --- Min Pulse Width ---
    tables = _tables_after_anchor(root, "MIN_PULSE_WIDTH_TABLE")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            report.min_pulse_width.append(
                MinPulseWidth(
                    number=_safe_int(row.get("Number", "0")),
                    slack_ns=_safe_float(row.get("Slack", "0")),
                    actual_width_ns=_safe_float(row.get("Actual Width", "0")),
                    required_width_ns=_safe_float(row.get("Required Width", "0")),
                    type=row.get("Type", ""),
                    clock=row.get("Clock", ""),
                    objects=row.get("Objects", ""),
                )
            )

    # --- Detailed Timing Paths (Setup + Hold) ---
    for analysis_anchor, analysis_type in [
        ("Setup_Analysis", "Setup"),
        ("Hold_Analysis", "Hold"),
    ]:
        _parse_detailed_paths(root, analysis_anchor, analysis_type, report)

    # --- High Fanout Nets ---
    tables = _tables_after_anchor(root, "High_Fanout_Nets_Report")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            report.high_fanout.append(
                HighFanoutNet(
                    fanout=_safe_int(row.get("FANOUT", "0")),
                    net_name=row.get("NET NAME", ""),
                    worst_slack_ns=_safe_float(row.get("WORST SLACK", "0")),
                    max_delay_ns=_safe_float(row.get("MAX DELAY", "0")),
                )
            )

    # --- Route Congestion ---
    tables = _tables_after_anchor(root, "Route_Congestions_Report")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            pct_str = row.get("ROUTE CONGESTIONS", "0").replace("%", "")
            report.route_congestion.append(
                RouteCongestion(
                    grid_loc=row.get("GRID LOC", ""),
                    congestion_pct=_safe_float(pct_str),
                )
            )

    # --- SDC Constraints ---
    tables = _tables_after_anchor(root, "SDC_Report")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            report.sdc_constraints.append(
                SDCConstraint(
                    command_type=row.get("SDC Command Type", ""),
                    state=row.get("State", ""),
                    detail_command=row.get("Detail Command", ""),
                )
            )


def _parse_detailed_paths(
    root: _Node,
    anchor_name: str,
    analysis_type: str,
    report: GowinTimingReport,
) -> None:
    """Parse all detailed timing paths under a Setup/Hold analysis section."""
    # Flatten DOM to find content between analysis anchors
    flat: list[_Node] = []
    stack = [root]
    while stack:
        node = stack.pop(0)
        flat.append(node)
        stack = list(node.children) + stack

    # Find anchor position
    start_idx = None
    for i, node in enumerate(flat):
        if node.tag == "a" and node.attrs.get("name") == anchor_name:
            start_idx = i
            break
    if start_idx is None:
        return

    # Find the end of this section (next h2 anchor or end of DOM)
    end_idx = len(flat)
    for i in range(start_idx + 1, len(flat)):
        node = flat[i]
        if node.tag == "h2":
            has_anchor = any(
                c.tag == "a" and c.attrs.get("name") for c in node.children
            )
            if has_anchor:
                end_idx = i
                break

    # Collect path data by scanning for h3 "PathN" markers
    section_nodes = flat[start_idx:end_idx]

    # Group tables by path number
    current_path_num = 0
    path_tables: dict[int, list[_Node]] = {}

    for node in section_nodes:
        if node.tag == "h3":
            text = node.get_text()
            m = re.match(r"Path\s*(\d+)", text)
            if m:
                current_path_num = int(m.group(1))
                path_tables[current_path_num] = []
        elif node.tag == "table" and current_path_num > 0:
            path_tables.setdefault(current_path_num, []).append(node)

    for path_num, tables in sorted(path_tables.items()):
        if len(tables) < 3:
            continue  # Need at least summary + arrival + required

        # Table 0: Path Summary (summary_table)
        summary_kv = _extract_kv_table(tables[0])
        summary = TimingPathSummary(
            slack_ns=_safe_float(summary_kv.get("Slack", "0")),
            data_arrival_time_ns=_safe_float(summary_kv.get("Data Arrival Time", "0")),
            data_required_time_ns=_safe_float(
                summary_kv.get("Data Required Time", "0")
            ),
            from_node=summary_kv.get("From", ""),
            to_node=summary_kv.get("To", ""),
            launch_clk=summary_kv.get("Launch Clk", ""),
            latch_clk=summary_kv.get("Latch Clk", ""),
        )

        # Table 1: Data Arrival Path
        arrival_steps = _parse_path_steps(tables[1])

        # Table 2: Data Required Path
        required_steps = _parse_path_steps(tables[2])

        # Table 3 (optional): Path Statistics
        stats = None
        if len(tables) >= 4:
            stats_kv = _extract_kv_table(tables[3])
            stats = TimingPathStats(
                clock_skew_ns=_safe_float(stats_kv.get("Clock Skew", "0")),
                setup_relationship_ns=_safe_float(
                    stats_kv.get("Setup Relationship", "0")
                ),
                logic_level=_safe_int(stats_kv.get("Logic Level", "0")),
                arrival_clock_path=stats_kv.get("Arrival Clock Path Delay", ""),
                arrival_data_path=stats_kv.get("Arrival Data Path Delay", ""),
                required_clock_path=stats_kv.get("Required Clock Path Delay", ""),
            )

        report.detailed_paths.append(
            DetailedTimingPath(
                analysis_type=analysis_type,
                path_number=path_num,
                summary=summary,
                arrival_path=arrival_steps,
                required_path=required_steps,
                statistics=stats,
            )
        )


def _parse_path_steps(table_node: _Node) -> list[TimingPathStep]:
    """Parse a Data Arrival / Data Required path table."""
    steps: list[TimingPathStep] = []
    for row in _extract_detail_table(table_node):
        steps.append(
            TimingPathStep(
                at_ns=_safe_float(row.get("AT", "0")),
                delay_ns=_safe_float(row.get("DELAY", "0")),
                type=row.get("TYPE", ""),
                rf=row.get("RF", ""),
                fanout=row.get("FANOUT", ""),
                loc=row.get("LOC", ""),
                node=row.get("NODE", ""),
            )
        )
    return steps


def parse_pnr_report(html_text: str, report: GowinTimingReport) -> None:
    """Parse project.rpt.html into the report object."""
    root = _parse_html(html_text)

    # --- Resource Usage ---
    tables = _tables_after_anchor(root, "Resource_Usage_Summary")
    for tbl in tables:
        for row in _extract_rows(tbl):
            if len(row) >= 3:
                report.resources.append(
                    ResourceUsage(
                        resource=row[0].strip(),
                        usage=row[1].strip(),
                        utilization=row[2].strip() if len(row) > 2 else "",
                    )
                )
            elif len(row) == 2:
                report.resources.append(
                    ResourceUsage(
                        resource=row[0].strip(),
                        usage=row[1].strip(),
                        utilization="",
                    )
                )

    # --- I/O Bank Usage ---
    tables = _tables_after_anchor(root, "I/O_Bank_Usage_Summary")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            report.io_banks.append(row)

    # --- Global Clock Signals ---
    tables = _tables_after_anchor(root, "Global_Clock_Signals")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            report.global_clocks.append(row)

    # --- Pin Assignments ---
    tables = _tables_after_anchor(root, "Pinout_by_Port_Name")
    for tbl in tables:
        rows = _extract_detail_table(tbl)
        for row in rows:
            # Skip header echo rows (first row may re-state column names)
            if row.get("Port Name") or row.get("col_0", "").strip() not in (
                "",
                "Port Name",
            ):
                report.pins.append(row)


def parse_power_report(html_text: str, report: GowinTimingReport) -> None:
    """Parse project.power.html into the report object."""
    root = _parse_html(html_text)

    # --- Power Info ---
    tables = _tables_after_anchor(root, "Power_Info")
    if tables:
        kv = _extract_kv_table(tables[0])
        report.power = PowerInfo(
            total_mw=_safe_float(kv.get("Total Power (mW)", "0")),
            quiescent_mw=_safe_float(kv.get("Quiescent Power (mW)", "0")),
            dynamic_mw=_safe_float(kv.get("Dynamic Power (mW)", "0")),
        )

    # --- Thermal Info ---
    tables = _tables_after_anchor(root, "Thermal_Info")
    if tables:
        kv = _extract_kv_table(tables[0])
        report.thermal = ThermalInfo(
            junction_temp_c=_safe_float(kv.get("Junction Temperature", "0")),
            theta_ja=_safe_float(kv.get("Theta JA", "0")),
            max_ambient_temp_c=_safe_float(
                kv.get("Max Allowed Ambient Temperature", "0")
            ),
        )

    # --- Supply Info ---
    tables = _tables_after_anchor(root, "Supply_Summary")
    for tbl in tables:
        for row in _extract_detail_table(tbl):
            report.supply.append(
                SupplyInfo(
                    source=row.get("Voltage Source", ""),
                    voltage_v=_safe_float(row.get("Voltage", "0")),
                    dynamic_current_ma=_safe_float(row.get("Dynamic Current(mA)", "0")),
                    quiescent_current_ma=_safe_float(
                        row.get("Quiescent Current(mA)", "0")
                    ),
                    power_mw=_safe_float(row.get("Power(mW)", "0")),
                )
            )


# ---------------------------------------------------------------------------
# Top-level parse function
# ---------------------------------------------------------------------------


def parse_build_dir(build_dir: str | Path) -> GowinTimingReport:
    """Parse all Gowin IDE report files from a build directory.

    Parameters
    ----------
    build_dir : str or Path
        Path to the Amaranth build directory (the one containing ``impl/``).

    Returns
    -------
    GowinTimingReport
        Structured report data from all parsed files.

    Raises
    ------
    FileNotFoundError
        If the build directory or ``impl/`` subdirectory does not exist.
    """
    build_dir = Path(build_dir)
    impl_dir = build_dir / "impl"
    if not impl_dir.is_dir():
        raise FileNotFoundError(
            f"No impl/ directory found in {build_dir}. Run the Gowin build first."
        )

    report = GowinTimingReport()

    # Timing report
    tr_file = impl_dir / "pnr" / "project_tr_content.html"
    if tr_file.exists():
        parse_timing_report(tr_file.read_text(errors="replace"), report)

    # PnR report
    pnr_file = impl_dir / "pnr" / "project.rpt.html"
    if pnr_file.exists():
        parse_pnr_report(pnr_file.read_text(errors="replace"), report)

    # Power report
    power_file = impl_dir / "pnr" / "project.power.html"
    if power_file.exists():
        parse_power_report(power_file.read_text(errors="replace"), report)

    return report


# ---------------------------------------------------------------------------
# Terminal rendering
# ---------------------------------------------------------------------------


def _header(title: str) -> str:
    return f"\n{'=' * 60}\n  {title}\n{'=' * 60}"


def _subheader(title: str) -> str:
    return f"\n--- {title} ---"


def render_summary(
    report: GowinTimingReport,
    sections: set[str] | None = None,
    max_paths: int = 3,
) -> str:
    """Render a concise terminal summary of the report.

    Parameters
    ----------
    report : GowinTimingReport
        Parsed report data.
    sections : set of str, optional
        Which sections to include.  If None, all sections are shown.
    max_paths : int
        Maximum number of detailed paths to show per analysis type.

    Returns
    -------
    str
        Formatted terminal output.
    """
    lines: list[str] = []
    show_all = sections is None

    def show(name: str) -> bool:
        return show_all or name in sections

    # --- Metadata ---
    if show("meta") and report.metadata:
        lines.append(_header("Build Information"))
        for key in (
            "Part Number",
            "Device",
            "Device Version",
            "Tool Version",
            "Created Time",
        ):
            val = report.metadata.get(key, "")
            if val:
                lines.append(f"  {key:.<35s} {val}")

    # --- STA Summary ---
    if show("meta") and report.sta_summary:
        lines.append(_subheader("STA Summary"))
        lines.append(
            f"  Delay Models: Setup={report.sta_summary.get('Setup Delay Model', '?')}"
            f"  Hold={report.sta_summary.get('Hold Delay Model', '?')}"
        )
        lines.append(
            f"  Paths Analyzed: {report.sta_summary.get('Numbers of Paths Analyzed', '?')}"
            f"  Endpoints: {report.sta_summary.get('Numbers of Endpoints Analyzed', '?')}"
        )
        violated_setup = report.sta_summary.get(
            "Numbers of Setup Violated Endpoints", "0"
        )
        violated_hold = report.sta_summary.get(
            "Numbers of Hold Violated Endpoints", "0"
        )
        any_violated = violated_setup != "0" or violated_hold != "0"
        marker = " *** VIOLATIONS ***" if any_violated else ""
        lines.append(
            f"  Violated: Setup={violated_setup}  Hold={violated_hold}{marker}"
        )

    # --- Clocks ---
    if show("clocks") and report.clocks:
        lines.append(_header("Clock Summary"))
        lines.append(
            f"  {'Name':<25s} {'Type':<8s} {'Period (ns)':>12s} {'Freq (MHz)':>12s}"
        )
        lines.append(f"  {'-' * 25} {'-' * 8} {'-' * 12} {'-' * 12}")
        for clk in report.clocks:
            lines.append(
                f"  {clk.name:<25s} {clk.type:<8s} "
                f"{clk.period_ns:>12.3f} {clk.frequency_mhz:>12.3f}"
            )

    # --- Fmax ---
    if show("fmax") and report.fmax:
        lines.append(_header("Max Frequency Report"))
        lines.append(
            f"  {'Clock':<25s} {'Constraint':>12s} {'Actual Fmax':>12s} {'Lvl':>4s} {'Status':>8s}"
        )
        lines.append(f"  {'-' * 25} {'-' * 12} {'-' * 12} {'-' * 4} {'-' * 8}")
        for f in report.fmax:
            status = "PASS" if f.met else "FAIL"
            marker = "" if f.met else " <---"
            lines.append(
                f"  {f.clock_name:<25s} "
                f"{f.constraint_mhz:>10.3f}  "
                f"{f.actual_fmax_mhz:>10.3f}  "
                f"{f.logic_level:>4d} "
                f"{status:>8s}{marker}"
            )

    # --- TNS ---
    if show("tns") and report.tns:
        lines.append(_header("Total Negative Slack"))
        lines.append(
            f"  {'Clock':<25s} {'Analysis':>8s} {'TNS (ns)':>10s} {'Endpoints':>10s}"
        )
        lines.append(f"  {'-' * 25} {'-' * 8} {'-' * 10} {'-' * 10}")
        for t in report.tns:
            flag = " <---" if t.endpoints_tns < 0 else ""
            lines.append(
                f"  {t.clock_name:<25s} {t.analysis_type:>8s} "
                f"{t.endpoints_tns:>10.3f} {t.num_endpoints:>10d}{flag}"
            )

    # --- Setup Slack ---
    if show("setup-slack") and report.setup_slack:
        lines.append(_header("Setup Slack (worst paths)"))
        _render_slack_table(lines, report.setup_slack)

    # --- Hold Slack ---
    if show("hold-slack") and report.hold_slack:
        lines.append(_header("Hold Slack (worst paths)"))
        _render_slack_table(lines, report.hold_slack)

    # --- Min Pulse Width ---
    if show("min-pulse-width") and report.min_pulse_width:
        lines.append(_header("Minimum Pulse Width"))
        lines.append(
            f"  {'#':>3s} {'Slack':>8s} {'Actual':>8s} {'Req':>8s} {'Type':<20s} {'Clock':<20s}"
        )
        lines.append(f"  {'-' * 3} {'-' * 8} {'-' * 8} {'-' * 8} {'-' * 20} {'-' * 20}")
        for pw in report.min_pulse_width:
            lines.append(
                f"  {pw.number:>3d} {pw.slack_ns:>8.3f} "
                f"{pw.actual_width_ns:>8.3f} {pw.required_width_ns:>8.3f} "
                f"{pw.type:<20s} {pw.clock:<20s}"
            )

    # --- Resources ---
    if show("resources") and report.resources:
        lines.append(_header("Resource Usage"))
        lines.append(f"  {'Resource':<30s} {'Usage':<40s} {'Util':>6s}")
        lines.append(f"  {'-' * 30} {'-' * 40} {'-' * 6}")
        for r in report.resources:
            # Skip header echo rows that got parsed as data
            if r.resource in ("Resource", "I/O Bank", "Clock Resource"):
                continue
            lines.append(f"  {r.resource:<30s} {r.usage:<40s} {r.utilization:>6s}")

    # --- I/O Banks ---
    if show("io-banks") and report.io_banks:
        lines.append(_header("I/O Bank Usage"))
        lines.append(f"  {'Bank':<12s} {'Usage':<12s} {'Util':>6s}")
        lines.append(f"  {'-' * 12} {'-' * 12} {'-' * 6}")
        for bank in report.io_banks:
            bname = bank.get("I/O Bank") or bank.get("col_0", "?")
            usage = bank.get("Usage") or bank.get("col_1", "?")
            util = bank.get("Utilization") or bank.get("col_2", "")
            if bname.strip() in ("", "I/O Bank"):
                continue
            lines.append(f"  {bname:<12s} {usage:<12s} {util:>6s}")

    # --- Global Clocks ---
    if show("global-clocks") and report.global_clocks:
        lines.append(_header("Global Clock Signals"))
        lines.append(f"  {'Signal':<25s} {'Global Clock':<15s} {'Location':<10s}")
        lines.append(f"  {'-' * 25} {'-' * 15} {'-' * 10}")
        for gc in report.global_clocks:
            sig = gc.get("Signal") or gc.get("col_0", "?")
            gclk = gc.get("Global Clock") or gc.get("col_1", "?")
            loc = gc.get("Location") or gc.get("col_2", "?")
            if sig.strip() in ("", "Signal"):
                continue
            lines.append(f"  {sig:<25s} {gclk:<15s} {loc:<10s}")

    # --- Pins ---
    if show("pins") and report.pins:
        lines.append(_header("Pin Assignments"))
        lines.append(f"  {'Port':<20s} {'Loc':>10s} {'Dir':<6s} {'IO Type':<12s}")
        lines.append(f"  {'-' * 20} {'-' * 10} {'-' * 6} {'-' * 12}")
        for p in report.pins:
            port = p.get("Port Name") or p.get("col_0", "?")
            loc = p.get("Loc./Bank") or p.get("col_2", "?")
            dir_ = p.get("Dir.") or p.get("col_4", "?")
            io_type = p.get("IO Type") or p.get("col_7", "?")
            if port.strip() in ("", "-", "Port Name"):
                continue
            lines.append(f"  {port:<20s} {loc:>10s} {dir_:<6s} {io_type:<12s}")

    # --- Power ---
    if show("power") and report.power:
        lines.append(_header("Power Summary"))
        lines.append(f"  Total Power ......... {report.power.total_mw:>10.3f} mW")
        lines.append(f"  Quiescent Power ..... {report.power.quiescent_mw:>10.3f} mW")
        lines.append(f"  Dynamic Power ....... {report.power.dynamic_mw:>10.3f} mW")

    # --- Thermal ---
    if show("thermal") and report.thermal:
        lines.append(_subheader("Thermal"))
        lines.append(
            f"  Junction Temp ....... {report.thermal.junction_temp_c:>10.3f} C"
        )
        lines.append(f"  Theta JA ............ {report.thermal.theta_ja:>10.3f}")
        lines.append(
            f"  Max Ambient Temp .... {report.thermal.max_ambient_temp_c:>10.3f} C"
        )

    # --- Supply ---
    if show("supply") and report.supply:
        lines.append(_subheader("Supply Rails"))
        lines.append(
            f"  {'Source':<10s} {'V':>6s} {'Idyn(mA)':>10s} {'Iq(mA)':>10s} {'P(mW)':>10s}"
        )
        lines.append(f"  {'-' * 10} {'-' * 6} {'-' * 10} {'-' * 10} {'-' * 10}")
        for s in report.supply:
            lines.append(
                f"  {s.source:<10s} {s.voltage_v:>6.3f} "
                f"{s.dynamic_current_ma:>10.3f} "
                f"{s.quiescent_current_ma:>10.3f} "
                f"{s.power_mw:>10.3f}"
            )

    # --- High Fanout ---
    if show("high-fanout") and report.high_fanout:
        # Filter out empty entries (padding rows from the HTML)
        real_hf = [hf for hf in report.high_fanout if hf.net_name.strip()]
        if real_hf:
            lines.append(_header("High Fanout Nets"))
            lines.append(
                f"  {'Fanout':>6s} {'Net':<30s} {'Worst Slack':>12s} {'Max Delay':>10s}"
            )
            lines.append(f"  {'-' * 6} {'-' * 30} {'-' * 12} {'-' * 10}")
            for hf in real_hf:
                lines.append(
                    f"  {hf.fanout:>6d} {hf.net_name:<30s} "
                    f"{hf.worst_slack_ns:>12.3f} {hf.max_delay_ns:>10.3f}"
                )

    # --- Route Congestion ---
    if show("congestion") and report.route_congestion:
        lines.append(_header("Route Congestion (top 10)"))
        for rc in report.route_congestion:
            lines.append(f"  {rc.grid_loc:<15s} {rc.congestion_pct:>6.1f}%")

    # --- SDC Constraints ---
    if show("sdc") and report.sdc_constraints:
        lines.append(_header("SDC Constraints"))
        for c in report.sdc_constraints:
            lines.append(f"  [{c.state}] {c.command_type}: {c.detail_command}")

    # --- Detailed Paths ---
    if show("paths") and report.detailed_paths:
        lines.append(_header("Detailed Timing Paths"))
        setup_paths = [p for p in report.detailed_paths if p.analysis_type == "Setup"]
        hold_paths = [p for p in report.detailed_paths if p.analysis_type == "Hold"]

        for label, paths in [("Setup", setup_paths), ("Hold", hold_paths)]:
            if not paths:
                continue
            lines.append(_subheader(f"{label} Paths (worst {max_paths})"))
            for path in paths[:max_paths]:
                s = path.summary
                lines.append(
                    f"  Path {path.path_number}: "
                    f"Slack={s.slack_ns:.3f} ns  "
                    f"{s.from_node} -> {s.to_node}  "
                    f"({s.launch_clk})"
                )
                if path.statistics:
                    st = path.statistics
                    lines.append(
                        f"    Logic Level={st.logic_level}  "
                        f"Clock Skew={st.clock_skew_ns:.3f} ns"
                    )
                    if st.arrival_data_path:
                        lines.append(f"    Data Path: {st.arrival_data_path}")

    return "\n".join(lines) + "\n"


def _render_slack_table(lines: list[str], entries: list[SlackEntry]) -> None:
    lines.append(
        f"  {'#':>3s} {'Slack':>8s} "
        f"{'From':<25s} {'To':<25s} "
        f"{'Skew':>6s} {'Delay':>7s}"
    )
    lines.append(f"  {'-' * 3} {'-' * 8} {'-' * 25} {'-' * 25} {'-' * 6} {'-' * 7}")
    for e in entries:
        flag = " <---" if e.slack_ns < 0 else ""
        lines.append(
            f"  {e.path_number:>3d} {e.slack_ns:>8.3f} "
            f"{e.from_node:<25s} {e.to_node:<25s} "
            f"{e.clock_skew_ns:>6.3f} {e.data_delay_ns:>7.3f}{flag}"
        )


# ---------------------------------------------------------------------------
# JSON serialisation
# ---------------------------------------------------------------------------


class _ReportEncoder(json.JSONEncoder):
    """JSON encoder that handles dataclass objects."""

    def default(self, o: Any) -> Any:
        if hasattr(o, "__dataclass_fields__"):
            return asdict(o)
        return super().default(o)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

ALL_SECTIONS = {
    "meta",
    "clocks",
    "fmax",
    "tns",
    "setup-slack",
    "hold-slack",
    "min-pulse-width",
    "resources",
    "io-banks",
    "global-clocks",
    "pins",
    "power",
    "thermal",
    "supply",
    "high-fanout",
    "congestion",
    "sdc",
    "paths",
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Extract timing reports from Gowin IDE HTML output.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Available sections: {', '.join(sorted(ALL_SECTIONS))}",
    )
    parser.add_argument(
        "build_dir",
        help="Path to the Amaranth build directory (containing impl/).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output full parsed data as JSON instead of terminal summary.",
    )
    parser.add_argument(
        "--section",
        action="append",
        dest="sections",
        metavar="NAME",
        help="Show only specific sections (repeatable). Omit to show all sections.",
    )
    parser.add_argument(
        "--paths",
        type=int,
        default=3,
        metavar="N",
        help="Max detailed paths to show per analysis type (default: 3).",
    )

    args = parser.parse_args(argv)

    try:
        report = parse_build_dir(args.build_dir)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(report, cls=_ReportEncoder, indent=2))
    else:
        selected = set(args.sections) if args.sections else None
        if selected:
            unknown = selected - ALL_SECTIONS
            if unknown:
                print(f"Warning: unknown sections: {unknown}", file=sys.stderr)
                selected -= unknown
        print(render_summary(report, sections=selected, max_paths=args.paths))

    return 0


if __name__ == "__main__":
    sys.exit(main())
