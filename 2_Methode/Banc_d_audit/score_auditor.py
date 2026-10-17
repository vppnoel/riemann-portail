#!/usr/bin/env python3
"""Notation d'un auditeur sur le corpus d'erreurs plantées : python audit_bench/score_auditor.py findings.json
findings.json = {"flagged": ["E01", "E05", ...]}  (identifiants signalés comme erronés)"""
import json, sys
from pathlib import Path

def score(flagged, corpus):
    errors = {e["id"] for e in corpus["errors"]}; decoys = {d["id"] for d in corpus["decoys"]}
    f = set(flagged); tp = f & errors; fa = f & decoys; unknown = f - errors - decoys
    fp = len(fa) + len(unknown)
    return dict(
        recall=len(tp) / len(errors), false_alarm_rate=len(fa) / len(decoys),
        precision=(len(tp) / (len(tp) + fp)) if (len(tp) + fp) else 0.0,
        missed=sorted(errors - f), false_alarms=sorted(fa), unknown_ids=sorted(unknown))

if __name__ == "__main__":
    corpus = json.load(open(Path(__file__).with_name("planted_errors.json"), encoding="utf-8-sig"))
    findings = json.load(open(sys.argv[1], encoding="utf-8-sig"))
    print(json.dumps(score(findings["flagged"], corpus), ensure_ascii=False, indent=1))
