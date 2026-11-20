"""Citation count, venue hint and the most-cited citing papers for one paper; no API key needed.

The fallback when the OpenAlex MCP is not connected (SKILL.md step 3).
Usage: python paper_meta.py 2605.21288               (arXiv ID; old style like hep-th/9711200 works too)
       python paper_meta.py 10.1038/s41586-024-08328-6   (DOI)
       python paper_meta.py --title "Attention Is All You Need"   (no ID or DOI: OpenAlex title search, check the match)
       python paper_meta.py 2605.21288 --citing 8     (also the 8 most-cited papers citing it, from OpenAlex)
IDs may also be given as "arXiv:2605.21288", an arxiv.org/abs or /pdf link, "doi:10...." or a doi.org link.
Prints JSON to stdout (UTF-8). Exit code 1 (with the errors printed) if no source answered. Runtime: ~1-30 s
(Semantic Scholar's keyless tier often rate-limits; it is retried with backoff before OpenAlex is tried).
Optional: a Semantic Scholar API key in the environment variable SEMANTIC_SCHOLAR_API_KEY is sent as the x-api-key
header (keys allow 1 request per second and still answer 429 now and then, so the backoff stays). The key is never
printed.
Python 3.8+ (no packages needed; use python3 where python is not on PATH).
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def get_json(url: str, tries: int = 3) -> dict:
    delay = 4
    headers = {"User-Agent": "paper-explainer"}
    s2_key = os.environ.get("SEMANTIC_SCHOLAR_API_KEY", "").strip()
    if s2_key and url.startswith("https://api.semanticscholar.org/"):
        headers["x-api-key"] = s2_key
    for attempt in range(1, tries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < tries:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError(f"no answer from {url}")


def citing_works(work_id: str, n: int) -> list[dict]:
    """The n most-cited works that cite this OpenAlex work; an arXiv and a published record of the same paper count once."""
    short = work_id.rsplit("/", 1)[-1]
    q = urllib.parse.urlencode({"filter": f"cites:{short}", "sort": "cited_by_count:desc", "per-page": min(2 * n, 200),
                                "select": "id,display_name,publication_year,cited_by_count,doi"})
    w = get_json(f"https://api.openalex.org/works?{q}")
    out, seen = [], set()
    for r in w.get("results", []):
        key = " ".join((r.get("display_name") or "").lower().split())
        if key in seen:
            continue
        seen.add(key)
        out.append({"title": r.get("display_name"), "year": r.get("publication_year"), "citations": r.get("cited_by_count"),
                    "doi": r.get("doi"), "openalex": r.get("id")})
    return out[:n]


def take_option(args: list[str], name: str) -> str | None:
    """Remove `name VALUE` from args and return VALUE (None when absent; ValueError when VALUE is missing)."""
    if name not in args:
        return None
    i = args.index(name)
    if i + 1 >= len(args):
        raise ValueError(f"{name} needs a value")
    value = args[i + 1]
    del args[i:i + 2]
    return value


def norm_title(s: str | None) -> str:
    return " ".join(re.sub(r"[^\w\s]", " ", (s or "").lower()).split())


def find_by_title(title: str) -> tuple[dict, bool]:
    """The OpenAlex work for a title: an exact (normalized) title match if there is one, else the top search hit."""
    q = urllib.parse.urlencode({"search": title, "per-page": 5,
                                "select": "id,display_name,publication_year,cited_by_count,doi,authorships"})
    results = get_json(f"https://api.openalex.org/works?{q}").get("results", [])
    if not results:
        raise RuntimeError(f"no OpenAlex work matches the title {title!r}")
    exact = [r for r in results if norm_title(r.get("display_name")) == norm_title(title)]
    return (exact[0] if exact else results[0]), bool(exact)


def normalize_id(raw: str) -> str:
    """Strip the usual wrappers: arXiv: prefix, arxiv.org abs/pdf links (and .pdf), doi: prefix, doi.org links."""
    s = raw.strip()
    s = re.sub(r"(?i)^(https?://)?(www\.|export\.)?arxiv\.org/(abs|pdf)/", "", s)
    s = re.sub(r"(?i)\.pdf$", "", s)
    s = re.sub(r"(?i)^arxiv:\s*", "", s)
    s = re.sub(r"(?i)^(https?://)?(dx\.)?doi\.org/", "", s)
    s = re.sub(r"(?i)^doi:\s*", "", s)
    return s.strip().rstrip("/")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # titles can hold any character; Windows pipes default to cp1252
    args = sys.argv[1:]
    try:
        citing = take_option(args, "--citing")
        title = take_option(args, "--title")
        n_citing = int(citing) if citing is not None else 0
    except ValueError:
        print(__doc__, file=sys.stderr)
        return 2
    if (title is None and len(args) != 1) or (title is not None and args):
        print(__doc__, file=sys.stderr)  # exactly one of: an ID / DOI, or --title
        return 2
    out = {"query": title or args[0].strip(), "checked": time.strftime("%Y-%m-%d"), "title_match": None,
           "semantic_scholar": None, "openalex": None, "citing": None, "errors": []}

    if title is not None:
        try:
            best, exact = find_by_title(title)
        except Exception as e:
            out["errors"].append(f"OpenAlex title search: {e}")
            print(json.dumps(out, ensure_ascii=False, indent=1))
            print("ERROR: no paper found for this title; ask the user for an ID, DOI or the PDF", file=sys.stderr)
            return 1
        out["title_match"] = {
            "title": best.get("display_name"), "year": best.get("publication_year"),
            "first_authors": [a.get("author", {}).get("display_name") for a in (best.get("authorships") or [])[:3]],
            "exact": exact, "note": "" if exact else "closest search hit, not an exact title match: check it is the right paper"}
        ident = normalize_id(best.get("doi") or "")
        if not ident:
            # No DOI: Semantic Scholar can't be asked by ID, OpenAlex answers from the search hit itself.
            out["errors"].append("Semantic Scholar: skipped, the matched work has no DOI")
            out["openalex"] = {"id": best.get("id"), "title": best.get("display_name"), "citations": best.get("cited_by_count"),
                               "year": best.get("publication_year"), "source": None, "note": "from the title search hit"}
            if n_citing > 0:
                try:
                    out["citing"] = citing_works(best["id"], n_citing)
                except Exception as e:
                    out["errors"].append(f"OpenAlex citing works: {e}")
            print(json.dumps(out, ensure_ascii=False, indent=1))
            return 0
    else:
        ident = normalize_id(args[0])

    # New-style (2401.12345) and old-style (hep-th/9711200) arXiv IDs; a DOI otherwise. An arXiv DOI counts as arXiv.
    ident = re.sub(r"(?i)^10\.48550/arxiv\.", "", ident)
    is_arxiv = re.fullmatch(r"(\d{4}\.\d{4,5}|[a-z][a-z.\-]*/\d{7})(v\d+)?", ident, flags=re.I) is not None
    arxiv_id = re.sub(r"v\d+$", "", ident) if is_arxiv else None
    if not is_arxiv and not ident.startswith("10."):
        print(f"ERROR: {ident!r} is neither an arXiv ID nor a DOI (DOIs start with 10.); use --title for a title",
              file=sys.stderr)
        return 2

    # DOIs may contain characters that mean something in a URL (#, ?, %, spaces): encode them, keep the slashes.
    s2_id = f"ARXIV:{arxiv_id}" if is_arxiv else f"DOI:{urllib.parse.quote(ident, safe='/')}"
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
        w = get_json(f"https://api.openalex.org/works/doi:{urllib.parse.quote(doi.lower(), safe='/')}")
        src = (w.get("primary_location") or {}).get("source") or {}
        # OpenAlex sometimes merges the arXiv record into the published one; only a record whose primary
        # source is still arXiv is the preprint-only count.
        arxiv_only = "arxiv" in (src.get("display_name") or "").lower()
        out["openalex"] = {"id": w.get("id"), "title": w.get("title"), "citations": w.get("cited_by_count"),
                           "year": w.get("publication_year"), "source": src.get("display_name"),
                           "note": "arXiv record only; usually undercounts versus Semantic Scholar, and a published "
                                   "version may have its own record" if arxiv_only else ""}
        if n_citing > 0:
            try:
                out["citing"] = citing_works(w["id"], n_citing)
            except Exception as e:
                out["errors"].append(f"OpenAlex citing works: {e}")
    except Exception as e:
        out["errors"].append(f"OpenAlex: {e}")

    print(json.dumps(out, ensure_ascii=False, indent=1))
    if out["semantic_scholar"] is None and out["openalex"] is None:
        print("ERROR: no citation source answered; show 'not available' on the page", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
