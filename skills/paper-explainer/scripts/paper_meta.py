"""Citation count and venue hint for one paper: Semantic Scholar first, OpenAlex as a labeled second source.

Usage: python paper_meta.py 2605.21288          (arXiv ID)
       python paper_meta.py 10.1038/s41586-024-08328-6   (DOI)
Prints JSON to stdout. Exit code 1 (with the errors printed) if no source answered. Runtime: ~1-30 s
(Semantic Scholar's keyless tier often rate-limits; it is retried with backoff before OpenAlex is tried).
"""
import json
import re
import sys
import time
import urllib.error
import urllib.request


def get_json(url: str, tries: int = 3) -> dict:
    delay = 4
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "paper-explainer"}), timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < tries:
                time.sleep(delay)
                delay *= 2
                continue
            raise


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__, file=sys.stderr)
        return 2
    ident = sys.argv[1].strip()
    is_arxiv = re.fullmatch(r"\d{4}\.\d{4,5}(v\d+)?", ident) is not None
    arxiv_id = re.sub(r"v\d+$", "", ident) if is_arxiv else None
    out = {"query": ident, "checked": time.strftime("%Y-%m-%d"), "semantic_scholar": None, "openalex": None, "errors": []}

    s2_id = f"ARXIV:{arxiv_id}" if is_arxiv else f"DOI:{ident}"
    try:
        w = get_json(f"https://api.semanticscholar.org/graph/v1/paper/{s2_id}"
                     "?fields=title,venue,year,citationCount,influentialCitationCount,publicationDate,publicationVenue")
        out["semantic_scholar"] = {"title": w.get("title"), "venue": w.get("venue"),
                                   "venue_name": (w.get("publicationVenue") or {}).get("name"),
                                   "year": w.get("year"), "date": w.get("publicationDate"),
                                   "citations": w.get("citationCount"), "influential": w.get("influentialCitationCount")}
    except Exception as e:  # reported, not swallowed: the caller decides what to show
        out["errors"].append(f"Semantic Scholar: {e}")

    doi = f"10.48550/arxiv.{arxiv_id}" if is_arxiv else ident
    try:
        w = get_json(f"https://api.openalex.org/works/doi:{doi.lower()}")
        src = (w.get("primary_location") or {}).get("source") or {}
        out["openalex"] = {"title": w.get("title"), "citations": w.get("cited_by_count"),
                           "year": w.get("publication_year"), "source": src.get("display_name"),
                           "note": "arXiv DOI record only; usually undercounts versus Semantic Scholar" if is_arxiv else ""}
    except Exception as e:
        out["errors"].append(f"OpenAlex: {e}")

    print(json.dumps(out, ensure_ascii=False, indent=1))
    if out["semantic_scholar"] is None and out["openalex"] is None:
        print("ERROR: no citation source answered; show 'not available' on the page", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
