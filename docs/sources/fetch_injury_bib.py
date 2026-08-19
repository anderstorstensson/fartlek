#!/usr/bin/env python3
"""Resolve exact CrossRef metadata for the running-injury review.

Same protocol as fetch_nutrition_bib.py: every DOI below was first seen in live
literature search output (or resolved by bibliographic query from a title seen
there, with the returned title checked by hand against the seed) — none was
reconstructed from memory. Fetched directly from CrossRef, which is
authoritative for authors, journal, year, volume, pages.

Prints JSON for manual review; writes nothing into the review document.

Caveat this script cannot address: DOI resolution proves the paper exists as
cited. It does NOT prove a quoted number appears in it. See §18 of the review
for which numeric claims were checked against source abstracts and which two
protocol figures carry secondary-source provenance.
"""
import json, sys, time, urllib.parse, urllib.request

UA = {"User-Agent": "fartlek-litreview/1.0 (mailto:torstensson.anders@gmail.com)"}

DOIS = {
    # Epidemiology, definition, risk factors
    "yamato2015def": "10.2519/jospt.2015.5741",
    "videbaek2015inc": "10.1007/s40279-015-0333-8",
    "vangent2007": "10.1136/bjsm.2006.033548",
    "lopes2012main": "10.1007/BF03262301",
    "desai2021history": "10.2519/jospt.2021.9673",
    "correia2024umbrella": "10.1016/j.jshs.2024.04.011",
    "vanderworp2015sex": "10.1371/journal.pone.0114937",
    "nielsen2013novice": "10.1177/2325967113487316",
    # Training load
    "nielsen2014progression": "10.2519/jospt.2014.5164",
    "buist2008gronorun": "10.1177/0363546507307505",
    "ramskov2018runclever": "10.1136/bmjsem-2017-000333",
    "soligard2016ioc": "10.1136/bjsports-2016-096581",
    "impellizzeri2020part2": "10.4085/1062-6050-501-19",
    "wang2020acwrlessons": "10.1007/s40279-020-01280-1",
    "zouhal2021acwred": "10.3389/fphys.2021.669687",
    "nakaoka2021dutch": "10.1007/s40279-021-01483-0",
    "frandsen2025runsafe": "10.2519/josptopen.2024.0075",
    "bahr2016screening": "10.1136/bjsports-2016-096256",
    # Bone stress injury
    "warden2014bsi": "10.2519/jospt.2014.5334",
    "fredericson1995mri": "10.1177/036354659502300418",
    "kijowski2012validation": "10.2214/AJR.11.6826",
    "ditmars2020recovery": "10.1007/s00247-020-04760-8",
    "george2024rtr": "10.1007/s40279-024-02051-y",
    "warden2021optimalload": "10.2519/jospt.2021.9982",
    "mcinnis2016highrisk": "10.1016/j.pmrj.2015.09.019",
    "aljanabi2023blackline": "10.5334/jbsr.3050",
    "mountjoy2023reds": "10.1136/bjsports-2023-106994",
    "joy2014triad": "10.1249/jsr.0000000000000077",
    "lappe2008calcium": "10.1359/jbmr.080102",
    # MTSS
    "reinking2016mtss": "10.1177/1941738116673299",
    "newman2013mtss": "10.2147/OAJSM.S39331",
    "winters2013mtsstx": "10.1007/s40279-013-0087-0",
    "marques2025mtssprev": "10.1016/j.gaitpost.2025.07.312",
    "withnall2006insoles": "10.1177/014107680609900113",
    "saad2025mtssscope": "10.7759/cureus.81463",
    # Tendinopathy
    "cook2009continuum": "10.1136/bjsm.2008.051193",
    "scott2020icon": "10.1136/bjsports-2019-100885",
    "alfredson1998ecc": "10.1177/03635465980260030301",
    "jonsson2008insertional": "10.1136/bjsm.2007.039545",
    "kongsgaard2009hsr": "10.1111/j.1600-0838.2009.00949.x",
    "beyer2015hsrvsecc": "10.1177/0363546515584760",
    "rio2015isometric": "10.1136/bjsports-2014-094386",
    "silbernagel2007painmonitor": "10.1177/0363546506298279",
    "vandervlist2020nma": "10.1136/bjsports-2019-101872",
    "challoumas2021patellar": "10.1136/bmjsem-2021-001110",
    "challoumas2023living": "10.1186/s40798-023-00616-1",
    "korakakis2026shockwave": "10.2519/jospt.2026.13985",
    "silbernagel2015rts": "10.2519/jospt.2015.5885",
    "chimenti2024cpg": "10.2519/jospt.2024.0302",
    "prudencio2023ecc": "10.1186/s13102-023-00618-2",
    # Plantar fasciopathy
    "rathleff2015highload": "10.1111/sms.12313",
    "koc2023heelcpg": "10.2519/jospt.2023.0303",
    # Patellofemoral pain
    "willy2019pfpcpg": "10.2519/jospt.2019.0302",
    "collins2018pfpconsensus": "10.1136/bjsports-2018-099397",
    "nascimento2018hipknee": "10.2519/jospt.2018.7365",
    "lankhorst2016prognosis": "10.1136/bjsports-2015-094664",
    # ITBS
    "fairclough2007itbs": "10.1016/j.jsams.2006.05.017",
    "sanchezalvarado2024itbs": "10.3389/fspor.2024.1386456",
    "aderem2015itbsbiomech": "10.1186/s12891-015-0808-7",
    # Calf and hamstring
    "green2025recurrence": "10.1136/bmjsem-2025-002865",
    "visser2025calfraise": "10.1016/j.bjpt.2025.101188",
    "vandyk2019nordic": "10.1136/bjsports-2018-100045",
    "impellizzeri2021nordicreappraisal": "10.1016/j.jclinepi.2021.09.007",
    "ripley2021compliance": "10.3390/ijerph182111260",
    "paton2023london3": "10.1136/bjsports-2021-105384",
    "hopkins2022ncaa": "10.1177/23259671211068079",
    "paganrosado2025calf": "10.1186/s40798-025-00960-4",
    # Prevention
    "lauersen2014prevention": "10.1136/bjsports-2013-092538",
    "lauersen2018strength": "10.1136/bjsports-2018-099078",
    "wu2024runnerprev": "10.1007/s40279-024-01993-7",
    "fokkema2019inspire": "10.1136/bjsports-2018-099744",
    "vanreijen2016compliance": "10.1007/s40279-016-0470-8",
    "patel2025fifa11": "10.7759/cureus.100463",
    # What is oversold
    "small2008stretching": "10.1080/15438620802310784",
    "anderson2022steprate": "10.1186/s40798-022-00504-0",
    "knapik2014archheight": "10.2519/jospt.2014.5342",
    "malisoux2016motioncontrol": "10.1136/bjsports-2015-095031",
    "willems2021pronation": "10.2519/jospt.2021.9710",
    "malisoux2020cushioning": "10.1177/0363546519892578",
    "ryan2014minimalist": "10.1136/bjsports-2012-092061",
    "bonanno2017orthoses": "10.1136/bjsports-2016-096671",
    # Red flags
    "finucane2020redflags": "10.2519/jospt.2020.9971",
    "tarabishi2023cecs": "10.7759/cureus.47797",
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
    out = {"by_doi": {}, "failed": []}
    for key, doi in DOIS.items():
        try:
            data = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
            out["by_doi"][key] = summarize(data["message"])
        except Exception as e:
            out["failed"].append({"key": key, "doi": doi, "error": str(e)})
        time.sleep(0.3)

    out["summary"] = {"requested": len(DOIS),
                      "resolved": len(out["by_doi"]),
                      "failed": len(out["failed"])}
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
