"""Regression tests for the Dealogic preview SQL safety boundary."""

import importlib.util
from pathlib import Path
import unittest


MODULE_PATH = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "imf-ra-data"
    / "scripts"
    / "dealogic.py"
)
SPEC = importlib.util.spec_from_file_location("dealogic", MODULE_PATH)
assert SPEC and SPEC.loader
DEALOGIC = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEALOGIC)


class ValidatePreviewSqlTests(unittest.TestCase):
    def test_accepts_bounded_top(self) -> None:
        DEALOGIC.validate_preview_sql(
            "SELECT TOP (20) DealNo FROM [Dealogic].[dbo].[DCMDeal]"
        )

    def test_rejects_top_percent(self) -> None:
        with self.assertRaisesRegex(ValueError, "TOP PERCENT"):
            DEALOGIC.validate_preview_sql(
                "SELECT TOP (20) PERCENT DealNo FROM [Dealogic].[dbo].[DCMDeal]"
            )

    def test_rejects_top_with_ties(self) -> None:
        with self.assertRaisesRegex(ValueError, "TOP WITH TIES"):
            DEALOGIC.validate_preview_sql(
                "SELECT TOP (20) WITH TIES DealNo "
                "FROM [Dealogic].[dbo].[DCMDeal] ORDER BY DealNo"
            )


if __name__ == "__main__":
    unittest.main()
