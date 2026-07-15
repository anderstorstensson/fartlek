#!/usr/bin/env python3
"""Query CrossRef for exact metadata of target citations. Prints for manual review."""
import json, time, urllib.parse, urllib.request

QUERIES = {
    "seiler2010": "Seiler What is Best Practice Training Intensity Duration Distribution Endurance Athletes",
    "stoggl2014": "Stoggl Sperlich polarized training endurance athletes superior high intensity",
    "casado2022pyr": "Casado Foster Ronnestad Tjelta pyramidal polarized training intensity distribution elite distance runners",
    "filipas2022": "Filipas pyramidal polarized training intensity distributions well-trained endurance runners 16 weeks",
    "rosenblatt2024": "Comparison Polarized Versus Other Types Endurance Training Intensity Distribution Endurance Performance Systematic Review Meta-analysis",
    "norwegian_slr": "Norwegian double-threshold method distance running systematic literature review",
    "tjelta2019": "Tjelta training characteristics world class distance runners lactate threshold",
    "casado2023review": "Casado Ronnestad training volume intensity distribution middle long distance runners narrative review",
    "hunter2025dur": "Hunter Maunder Jones Durability index endurance exercise performance methodological considerations",
    "jones2025resil": "Jones physiological resilience what is it how might it be trained",
    "maunder2021dur": "Maunder Seiler Mitchell Durability endurance athletes new metric",
    "jones2024fourth": "Jones fourth dimension physiological resilience durability endurance",
    "pettitt2016cs": "Pettitt Applying Critical Speed Concept Racing Strategy Interval Training Prescription",
    "jones2019cp": "Jones Burnley Black Poole Vanhatalo maximal metabolic steady state redefining boundaries",
    "vanhatalo2016cp": "Jones Vanhatalo critical power implications determination VO2max exercise tolerance",
    "llanos2024econ": "Strength Training Programs Middle Long Distance Runners Economy Different Running Speeds Systematic Review Meta-analysis",
    "blagrove2018": "Blagrove Howatson Hayes Effects Strength Training Physiological Determinants Middle Long Distance Running Performance Systematic Review",
    "denadai2017": "Denadai Explosive heavy strength training running economy endurance runners meta-analysis",
    "barnes2015econ": "Barnes Kilding Running economy factors affecting measurement",
    "hoogkamer2018": "Hoogkamer Kipp Frank Farina Luo Kram comparison metabolic cost running prototype racing shoe",
    "aft_review2024": "Mechanisms Economy Performance Advanced Footwear Technology Endurance Running Review",
    "impellizzeri2020": "Impellizzeri Woodcock Coutts Acute Chronic Workload Ratio Conceptual Issues Fundamental Pitfalls",
    "impellizzeri2021flaw": "Impellizzeri acute-chronic workload ratio-injury figure sweet spot flawed",
    "lolli2019": "Lolli Batterham Hawkins Kelly Acute chronic workload ratio ratios injury",
    "bosquet2007taper": "Bosquet Montpetit Arvisais Mujika Effects tapering performance meta-analysis",
    "spilsbury2023taper": "Effects tapering performance endurance athletes systematic review meta-analysis 2023",
    "impey2018fuel": "Impey Hearris Hammond Fuel Work Required Carbohydrate Periodization Glycogen Threshold Hypothesis",
    "gejl2021cho": "Performance effects periodized carbohydrate restriction endurance trained athletes systematic review meta-analysis",
    "jeukendrup2014cho": "Jeukendrup step towards personalized sports nutrition carbohydrate intake during exercise",
    "hrv_meta2021": "Heart Rate Variability-Guided Training Enhancing Cardiac-Vagal Modulation Aerobic Fitness Endurance Performance Systematic Review Meta-Analysis",
    "duking2021hrv": "Duking Monitoring adapting endurance training heart rate variability wearable technologies systematic review meta-analysis",
    "mcnulty2020mc": "McNulty Effects Menstrual Cycle Phase Exercise Performance Eumenorrheic Women Systematic Review Meta-Analysis",
    "mountjoy2023reds": "Mountjoy 2023 International Olympic Committee IOC consensus statement Relative Energy Deficiency Sport REDs",
    "billat2001": "Billat Interval training performance scientific bases special forms interval training",
    "midgley2007": "Midgley McNaughton Wilkinson Training to enhance metabolic determinants endurance running performance",
    "bellinger2020": "Critical power interval training endurance performance",
}

def fetch(q):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({
        "query.bibliographic": q, "rows": 1,
        "select": "DOI,title,author,published,container-title,is-referenced-by-count"
    })
    req = urllib.request.Request(url, headers={"User-Agent": "litreview/1.0 (mailto:torstensson.anders@gmail.com)"})
    with urllib.request.urlopen(req, timeout=20) as r:
        data = json.load(r)
    items = data["message"]["items"]
    if not items:
        return None
    it = items[0]
    auth = it.get("author", [])
    first = auth[0].get("family", "?") + (" et al." if len(auth) > 1 else "") if auth else "?"
    yr = it.get("published", {}).get("date-parts", [[None]])[0][0]
    return {
        "doi": it.get("DOI"), "first_author": first,
        "year": yr, "title": it.get("title", ["?"])[0],
        "journal": (it.get("container-title") or ["?"])[0],
        "cites": it.get("is-referenced-by-count"),
    }

out = {}
for key, q in QUERIES.items():
    try:
        out[key] = fetch(q)
        print(f"{key}: {out[key]['year']} | {out[key]['first_author']} | {out[key]['title'][:70]} | {out[key]['journal'][:40]} | doi:{out[key]['doi']} | cites:{out[key]['cites']}")
    except Exception as e:
        print(f"{key}: ERROR {e}")
        out[key] = None
    time.sleep(0.4)

with open("/media/anders/work/runApp/docs/sources/bibliography_raw.json", "w") as f:
    json.dump(out, f, indent=2)
print("\nSaved bibliography_raw.json")
