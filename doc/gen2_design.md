# Gen2 (10 Gbps / SuperSpeedPlus) design note — MERGED

**This note has been merged into `doc/usb3_design.md`** (the unified
dual-rate × dual-lane × width-generic design: LUNA `core_width ∈
{32,64,128}`, PHY PIPE `{64,128}`, Gen 1x1/Gen 1x2/Gen 2x1 at both PIPE
widths, Gen 2x2 at 128).

Historical mapping for references in HANDOVER/prompt (the exact text as
executed through gates G0–G4 and session 13 lives in git history,
last full version at fork commit `4d21789`):

* §1 width/clock plan (stage A/B) → superseded by `usb3_design.md` §1/§4
  (stage A relationship: §10)
* §2 framing delta + SSP link deltas → `usb3_design.md` §6 (statuses
  updated: G3/G4-closed)
* §3 LTSSM delta → `usb3_design.md` §5
* §4 PIPE boundary + §9.1 pinned contract → `usb3_design.md` §3.4/§8
* §5 timing budget → `usb3_design.md` §7 (measured session-13 anchors)
* §6 SKP x=4 quirk → `usb3_design.md` §3.4
* §7 enumeration surface → `usb3_design.md` §8
* §8 sim shape → `usb3_design.md` §9
