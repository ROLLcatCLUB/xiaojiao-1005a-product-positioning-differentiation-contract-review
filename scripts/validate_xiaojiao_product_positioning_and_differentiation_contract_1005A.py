from __future__ import annotations
import argparse, json, sys, zipfile
from pathlib import Path
STAGE="1005A_XIAOJIAO_PRODUCT_POSITIONING_AND_DIFFERENTIATION_CONTRACT"
FINAL="XIAOJIAO_PRODUCT_POSITIONING_AND_DIFFERENTIATION_CONTRACT_PASS"
SLUG="xiaojiao_product_positioning_and_differentiation_contract_1005A"
MARKER="ALL_1005A_XIAOJIAO_PRODUCT_POSITIONING_AND_DIFFERENTIATION_CONTRACT_CHECKS_OK"
BAD=[".env","token","secret","key","node_modules","__pycache__",".db",".sqlite","dist","build","coverage",".DS_Store"]
REQUIRED_PRINCIPLES={"state_before_function","object_before_page","continuity_before_single_generation","layered_focus_surface_and_complex_studio","resources_and_knowledge_as_support_layer","analysis_must_flow_back_to_action","teacher_retains_authority"}
def fail(m): raise SystemExit(f"VALIDATION_FAILED: {m}")
def load(p): return json.loads(p.read_text(encoding="utf-8-sig"))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--root"); a=ap.parse_args(); root=Path(a.root).resolve() if a.root else Path(__file__).resolve().parents[1]
    req=[f"docs/foundation/{SLUG}.md",f"docs/foundation/{SLUG}.json",f"samples/{SLUG}/product_positioning_guardrail_sample_1005A.json",f"docs/audit/{SLUG}_result.json",f"docs/audit/{SLUG}_report.md",f"docs/audit_packages/{SLUG}_manifest.json",f"scripts/validate_{SLUG}.py"]
    for r in req:
        if not (root/r).exists(): fail(f"missing required file: {r}")
    c=load(root/f"docs/foundation/{SLUG}.json"); s=load(root/f"samples/{SLUG}/product_positioning_guardrail_sample_1005A.json"); r=load(root/f"docs/audit/{SLUG}_result.json"); m=load(root/f"docs/audit_packages/{SLUG}_manifest.json")
    if c.get("stage_code")!=STAGE or s.get("stage_code")!=STAGE or r.get("stage_code")!=STAGE: fail("stage mismatch")
    if c.get("final_status_target")!=FINAL or r.get("final_status")!=FINAL or r.get("marker")!=MARKER or r.get("pass") is not True: fail("result mismatch")
    if c.get("first_identity")!="teacher_work_state_driven_intelligent_organization_system": fail("first identity mismatch")
    for forbidden in ["AI lesson generator","PPT/courseware generator","smart classroom platform","resource library / knowledge base","student evaluation board","school digitization backend"]:
        if forbidden not in c.get("not_first_identity",[]): fail(f"missing not first identity {forbidden}")
    if set(c.get("differentiation_principles",[])) != REQUIRED_PRINCIPLES: fail("principles mismatch")
    for key in ["1001","1000F_I","1002","1003","1004","resource_library"]:
        if key not in c.get("route_constraints",{}): fail(f"missing route constraint {key}")
    if len(c.get("competitor_collision_guards",[])) < 6: fail("collision guards too few")
    if len(s.get("feature_route_checks",[])) < 5: fail("feature route checks too few")
    for mapping in [c.get("hard_boundaries",{}), s.get("boundary_flags",{}), r.get("boundary_flags",{})]:
        for k,v in mapping.items():
            if v is not False: fail(f"unsafe boundary {k}")
    z=root/f"docs/audit_packages/{SLUG}.zip"
    if not z.exists(): fail("missing zip")
    with zipfile.ZipFile(z) as zf: entries=zf.namelist()
    for e in entries:
        n=e.replace("\\","/")
        if n.startswith("/") or ":" in n or "\\" in e: fail(f"unsafe zip path {e}")
        if any(b.lower() in n.lower() for b in BAD): fail(f"forbidden zip entry {e}")
    if m.get("manifest_minus_zip")!=[] or m.get("zip_minus_manifest")!=[] or sorted(m.get("zip_entries",[]))!=sorted(entries): fail("manifest mismatch")
    print(MARKER); return 0
if __name__=="__main__": sys.exit(main())