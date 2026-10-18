# Real asset sourcing

## Wikimedia Commons (best general source)
```bash
python3 tools/commons.py search "thuluth calligraphy" 40       # size · licence · title · artist
python3 tools/commons.py get "File:Exact name.jpg" assets/real/panel.jpg 2560
```
- Raw API: `https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srlimit=30&format=json&srsearch=...`
  then `prop=imageinfo&iiprop=url|size|extmetadata` for URL + licence.
- Download with `Special:FilePath/<name>?width=2560` or the original URL. Arbitrary thumb widths (2400px-) → 2 KB errors.
- Good search patterns: `"<topic>" manuscript`, `"<artist> hilye"`, `"<museum> <object id>"`, category names
  (e.g. "Category:Thuluth"), Arabic/Turkish/Persian spellings too.

## Museum open access
- The Met (CC0, api: collectionapi.metmuseum.org), Walters Art Museum (CC0), Freer|Sackler / Smithsonian Open
  Access (CC0), Rijksmuseum (CC0), Library of Congress (PD), British Library (PD on Flickr/Commons),
  David Collection (CC BY), Chester Beatty (some CC), Qatar Digital Library (open licence).
- Prefer full-page, high-res scans; crops come later.

## What to fetch per topic (checklist)
- The thing itself at its best (masterpiece examples, ≥3000 px).
- The people (photos; if none → AI portrait reconstruction).
- The places (archival photos of buildings/cities).
- The tools/process (photos of instruments, workshops).
- Evidence for each claim in the VO (a date, an inscription, a document).

## Licences
PD / CC0: free. CC BY / CC BY-SA: credit in `docs/CREDITS.md` and in the release notes. Avoid NC/ND for
public monetised videos unless the user accepts. No random Google Images.

## Gaps
No photo exists → AI (see prompt_templates.md). Object too generic to search (e.g. a penknife) → generate
and cut out. Never fake an artefact that really exists — find the real one.
