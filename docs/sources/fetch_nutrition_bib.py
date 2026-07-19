#!/usr/bin/env python3
"""Resolve exact CrossRef metadata for the sports-nutrition review.

Two input modes, both seeded from live web-search results rather than recall:
  DOIS   — DOI found in search results; fetched directly (authoritative).
  TITLES — exact title string found in search results but no DOI surfaced;
           queried bibliographically, then the returned title MUST be checked
           by hand against the seed before the reference is used.
Prints JSON for manual review; writes nothing into the review document.
"""
import json, sys, time, urllib.parse, urllib.request

UA = {"User-Agent": "fartlek-litreview/1.0 (mailto:torstensson.anders@gmail.com)"}
SELECT = "DOI,title,author,published,container-title,volume,issue,page,is-referenced-by-count,type"

DOIS = {
    "ioc2018supp": "10.1136/bjsports-2018-099027",
    "grgic2020umbrella": "10.1136/bjsports-2018-100278",
    "guest2021caf": "10.1186/s12970-020-00383-4",
    "kreider2017cre": "10.1186/s12970-017-0173-z",
    "hill2021cherry": "10.1123/ijsnem.2020-0145",
    "cherry2026meta": "10.1186/s40798-026-00993-3",
    "broccoli2026acute": "10.3390/antiox15030379",
    "paulsen2014": "10.1113/jphysiol.2013.267419",
    "jager2017prot": "10.1186/s12970-017-0177-8",
    "grgic2021bicarb": "10.1186/s12970-021-00458-w",
    "trexler2015ba": "10.1186/s12970-015-0090-y",
    "margolis2021glyc": "10.1186/s40798-020-00297-0",
    "eah2015": "10.1097/JSM.0000000000000221",
    "parr2014alcohol": "10.1371/journal.pone.0088384",
    "thomas2016acsm": "10.1016/j.jand.2015.12.006",
    "kato2016prot": "10.1371/journal.pone.0157406",
    "forbes2023cre": "10.1080/15502783.2023.2204071",
    "cyp1a2srev": "10.1007/s00394-020-02427-6",
    "gardiner2025sleep": "10.1093/sleep/zsae230",
    "beetumbrella2025": "10.3390/nu17121958",
    "cherrysleep2022": "10.3390/ijerph191610272",
    "adrv2022": "10.3389/fspor.2022.868228",
    "recovery2025narr": "10.1007/s40279-025-02213-6",
    "protend2025": "10.1007/s40279-025-02203-8",
    "caffsleeptrain2025": "10.3390/sports13090317",
}

# Exact titles as they appeared in search results (no DOI surfaced).
TITLES = {
    "shaw2017gelatin": "Vitamin C-enriched gelatin supplementation before intermittent activity augments collagen synthesis",
    "ketones2022meta": "Acute Ingestion of Ketone Monoesters and Precursors Do Not Enhance Endurance Exercise Performance: A Systematic Review and Meta-Analysis",
    "nitrate2022tt": "The effects of nitrate ingestion on high-intensity endurance time-trial performance: A systematic review and meta-analysis",
    "vitd2021": "Vitamin D in athletes: focus on physical performance and musculoskeletal injuries",
    "iron2024female": "Iron deficiency, supplementation, and sports performance in female athletes: A systematic review",
    "broccoli2023train": "Glucosinolate-rich broccoli sprouts protect against oxidative stress and improve adaptations to intense exercise training",
    "caffsleepmeta2023": "The effect of caffeine on subsequent sleep: A systematic review and meta-analysis",
    "cherryprecovery2022": "Precovery versus recovery: Understanding the role of cherry juice in exercise recovery",
    "antiox2020muscle": "Do antioxidant supplements interfere with skeletal muscle adaptation to exercise training?",
    "caffrun2022meta": "Effects of Caffeine Intake on Endurance Running Performance and Time to Exhaustion: A Systematic Review and Meta-Analysis",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return json.load(r)


def summarize(it):
    auth = it.get("author", [])
    names = [a.get("family", a.get("name", "?")) for a in auth]
    pub = it.get("published", {}).get("date-parts", [[None]])[0]
    return {
        "doi": it.get("DOI"),
        "title": (it.get("title") or ["?"])[0],
        "authors": names[:6],
        "n_authors": len(names),
        "year": pub[0] if pub else None,
        "journal": (it.get("container-title") or ["?"])[0],
        "volume": it.get("volume"),
        "issue": it.get("issue"),
        "page": it.get("page"),
        "cited_by": it.get("is-referenced-by-count"),
        "type": it.get("type"),
    }


def main():
    out = {"by_doi": {}, "by_title": {}, "failed": []}
    for key, doi in DOIS.items():
        try:
            data = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
            out["by_doi"][key] = summarize(data["message"])
        except Exception as e:
            out["failed"].append({"key": key, "doi": doi, "error": str(e)})
        time.sleep(0.3)

    for key, title in TITLES.items():
        try:
            url = "https://api.crossref.org/works?" + urllib.parse.urlencode(
                {"query.bibliographic": title, "rows": 2, "select": SELECT})
            items = get(url)["message"]["items"]
            out["by_title"][key] = {"seed_title": title,
                                    "candidates": [summarize(i) for i in items]}
        except Exception as e:
            out["failed"].append({"key": key, "title": title, "error": str(e)})
        time.sleep(0.3)

    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
