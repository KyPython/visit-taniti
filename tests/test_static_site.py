"""Independent static-site fault fixtures for SITE-QA-1 through SITE-QA-7."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "check_static_site.py"
PAGE = '<!DOCTYPE html><html lang="en"><head><title>Fixture</title></head><body><main id="main">{}</main></body></html>'


class StaticSiteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "site"
        self.root.mkdir()

    def write(self, name, content):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def run_checker(self):
        result = subprocess.run(
            [sys.executable, "-B", str(CHECKER), "--root", str(self.root)],
            capture_output=True, text=True, check=False, timeout=10,
        )
        self.assertEqual(result.stderr, "", result.stderr)
        return result

    def test_SITE_QA_3_valid_relative_root_fragment_query_and_external_links(self):
        self.write("index.html", PAGE.format(
            '<a href="book.html?type=hotel#r%C3%A9sum%C3%A9">Book</a>'
            '<a href="/index.html#main">Home</a><a href="#main">Skip</a>'
            '<a href="https://example.invalid/not-fetched">External</a>'
            '<img src="//example.invalid/not-fetched.png">'
            '<a href="mailto:test@example.invalid">Email</a>'
            '<script src="js/site.js?v=2"></script>'
        ))
        self.write("book.html", PAGE.format('<p id="résumé">Booking</p>'))
        self.write("js/site.js", "void 0;")
        result = self.run_checker()
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_SITE_QA_1_3_missing_pages_and_assets_fail_even_with_query(self):
        for reference in ("missing.html?type=hotel", "missing.css", "missing.js", "missing.png"):
            with self.subTest(reference=reference):
                self.write("index.html", PAGE.format(f'<a href="{reference}">Target</a>'))
                result = self.run_checker()
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn("local target does not exist", result.stdout)

    def test_SITE_QA_3_missing_fragment_in_existing_document_fails(self):
        self.write("index.html", PAGE.format('<a href="book.html#missing">Book</a>'))
        self.write("book.html", PAGE.format(""))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("local fragment does not exist", result.stdout)

    def test_SITE_QA_2_duplicate_ids_fail(self):
        self.write("index.html", PAGE.format('<p id="main">Duplicate</p>'))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate ID", result.stdout)

    def test_SITE_QA_2_missing_structure_fails(self):
        cases = (
            (PAGE.format("").replace("<!DOCTYPE html>", ""), "missing HTML doctype"),
            (PAGE.format("").replace('lang="en"', 'lang=""'), "missing document language"),
            (PAGE.format("").replace("Fixture", " "), "missing document title"),
            (PAGE.format("").replace("<main id=\"main\"></main>", ""), "expected one main landmark"),
            (PAGE.format("<main></main>"), "expected one main landmark"),
            (PAGE.format('<div role="main"></div>'), "expected one main landmark"),
        )
        for content, diagnostic in cases:
            with self.subTest(diagnostic=diagnostic):
                self.write("index.html", content)
                result = self.run_checker()
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn(diagnostic, result.stdout)

    def test_SITE_QA_4_path_escape_fails_even_when_outside_file_exists(self):
        outside = self.root.parent / "outside.html"
        outside.write_text(PAGE.format(""), encoding="utf-8")
        for reference in ("../outside.html", "%2e%2e/outside.html"):
            with self.subTest(reference=reference):
                self.write("index.html", PAGE.format(f'<a href="{reference}">Escape</a>'))
                result = self.run_checker()
                self.assertEqual(result.returncode, 1)
                self.assertIn("escapes the site root", result.stdout)

    def test_SITE_QA_4_symlink_escape_fails(self):
        outside = self.root.parent / "outside.html"
        outside.write_text(PAGE.format(""), encoding="utf-8")
        (self.root / "escape.html").symlink_to(outside)
        self.write("index.html", PAGE.format('<a href="escape.html">Escape</a>'))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("escapes the site root", result.stdout)

    def test_SITE_QA_4_path_case_must_match_even_on_macos(self):
        self.write("book.html", PAGE.format(""))
        self.write("index.html", PAGE.format('<a href="BOOK.html">Book</a>'))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, result.stdout)

    def test_SITE_QA_7_empty_site_is_a_failure(self):
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("No root HTML pages", result.stdout)

    def test_SITE_QA_2_uppercase_html_extension_is_checked(self):
        self.write("index.html", PAGE.format(""))
        self.write("other.HTML", "<html><body>Missing required structure</body></html>")
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("other.HTML: missing HTML doctype", result.stdout)

    def test_SITE_QA_4_symlink_target_case_must_match(self):
        self.write("book.html", PAGE.format(""))
        (self.root / "alias.html").symlink_to("BOOK.html")
        self.write("index.html", PAGE.format('<a href="alias.html#main">Book</a>'))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)

    def test_SITE_QA_3a_base_url_is_explicitly_rejected(self):
        self.write("index.html", PAGE.format('<base href="nested/"><a href="book.html">Book</a>'))
        self.write("book.html", PAGE.format(""))
        self.write("nested/index.html", PAGE.format(""))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("base href is unsupported", result.stdout)

    def test_SITE_QA_3a_file_urls_are_not_silently_skipped(self):
        self.write("index.html", PAGE.format('<a href="file:///missing.html">Local file</a>'))
        result = self.run_checker()
        self.assertEqual(result.returncode, 1)
        self.assertIn("file URLs are not deployable", result.stdout)


if __name__ == "__main__":
    unittest.main()
