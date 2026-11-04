"""Offline checks for the root HTML pages; see docs/static-site-quality.md."""

import argparse
import os
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Document(HTMLParser):
    def __init__(self, content):
        super().__init__(convert_charrefs=True)
        self.doctype = False
        self.language = ""
        self.title = []
        self.in_title = False
        self.main_count = 0
        self.ids = set()
        self.duplicate_ids = set()
        self.references = []
        self.has_base = False
        self.feed(content)
        self.close()

    def handle_decl(self, decl):
        if decl.lower().split() == ["doctype", "html"]:
            self.doctype = True

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "base" and "href" in attributes:
            self.has_base = True
        if tag == "html":
            self.language = (attributes.get("lang") or "").strip()
        if tag == "title":
            self.in_title = True
        if tag == "main" or (attributes.get("role") or "").strip().lower() == "main":
            self.main_count += 1
        if "id" in attributes:
            identifier = attributes["id"] or ""
            if identifier in self.ids:
                self.duplicate_ids.add(identifier)
            self.ids.add(identifier)
        for name in ("href", "src"):
            if name in attributes:
                self.references.append((attributes[name] or "", self.getpos()[0]))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def read_document(path):
    return Document(path.read_text(encoding="utf-8"))


def exact_path_case(root, candidate):
    """Detect Linux deploy failures even when the local filesystem ignores case."""
    relative = Path(os.path.normpath(candidate)).relative_to(root)
    cursor = root
    for part in relative.parts:
        if part not in {entry.name for entry in cursor.iterdir()}:
            return False
        cursor /= part
    return True


def check_reference(root, source, reference, documents):
    parsed = urlsplit(reference)
    if parsed.scheme.lower() == "file":
        return "file URLs are not deployable site references"
    if parsed.scheme or parsed.netloc:
        return None
    path = unquote(parsed.path)
    if path.startswith("/"):
        candidate = root / path.lstrip("/")
    elif path:
        candidate = source.parent / path
    else:
        candidate = source
    resolved = candidate.resolve()
    if not resolved.is_relative_to(root):
        return "local target escapes the site root"
    if resolved.is_dir():
        candidate /= "index.html"
        resolved = candidate.resolve()
        if not resolved.is_relative_to(root):
            return "local target escapes the site root"
    if not resolved.is_file():
        return "local target does not exist"
    if not exact_path_case(root, candidate):
        return "local target has incorrect path case"
    if not exact_path_case(root, resolved):
        return "symlink target has incorrect path case"
    if parsed.fragment and resolved.suffix.lower() in {".html", ".svg"}:
        if resolved not in documents:
            documents[resolved] = read_document(resolved)
        if unquote(parsed.fragment) not in documents[resolved].ids:
            return "local fragment does not exist"
    return None


def check_site(site_root):
    root = Path(site_root).resolve()
    errors = []
    pages = sorted(page for page in root.iterdir() if page.suffix.lower() == ".html")
    if not pages:
        return ["No root HTML pages found."], 0, 0
    documents = {}
    for page in pages:
        if not page.resolve().is_relative_to(root):
            errors.append(f"{page.name}: HTML page escapes the site root")
            continue
        try:
            if not exact_path_case(root, page.resolve()):
                errors.append(f"{page.name}: symlink target has incorrect path case")
                continue
            doc = read_document(page)
        except (OSError, UnicodeError, ValueError) as error:
            errors.append(f"{page.name}: cannot parse document: {error}")
            continue
        documents[page.resolve()] = doc
        if doc.has_base:
            errors.append(f"{page.name}: base href is unsupported; resolve URLs with a browser check")
        if not doc.doctype:
            errors.append(f"{page.name}: missing HTML doctype")
        if not doc.language:
            errors.append(f"{page.name}: missing document language")
        if not "".join(doc.title).strip():
            errors.append(f"{page.name}: missing document title")
        if doc.main_count != 1:
            errors.append(f"{page.name}: expected one main landmark, found {doc.main_count}")
        for identifier in sorted(doc.duplicate_ids):
            errors.append(f"{page.name}: duplicate ID {identifier!r}")
    reference_count = 0
    for page in pages:
        doc = documents.get(page.resolve())
        if doc is None:
            continue
        for reference, line in doc.references:
            reference_count += 1
            try:
                problem = check_reference(root, page, reference, documents)
            except (OSError, UnicodeError, ValueError, RuntimeError) as error:
                problem = f"invalid local reference: {error}"
            if problem:
                errors.append(f"{page.name}:{line}: {reference!r}: {problem}")
    return errors, len(pages), reference_count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = parser.parse_args()
    errors, page_count, reference_count = check_site(args.root)
    for error in errors:
        print(f"FAIL {error}")
    print(f"Checked {page_count} pages and {reference_count} references; {len(errors)} failures.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
