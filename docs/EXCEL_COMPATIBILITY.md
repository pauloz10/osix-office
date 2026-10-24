# Excel-first compatibility plan

Priority order:

1. XLSX open/edit/save without format conversion prompts.
2. Formula compatibility and cached formula preservation.
3. Tables, named ranges, conditional formatting, data validation and charts.
4. Pivot tables, filters, freeze panes and print areas.
5. XLSM round-trip preservation.
6. VBA execution fallback through a separately installed LibreOffice compatibility mode where feasible.
7. Regression tests using real workbooks created in Microsoft Excel.

## Important limitation

Euro-Office/ONLYOFFICE-style macros use JavaScript, not VBA. XLSM documents can be edited, but VBA execution is not natively equivalent to Microsoft Excel. LibreOffice can execute a useful but incomplete subset of VBA.

## Test corpus

Place non-sensitive copies of representative workbooks into `tests/corpus/` and run:

```bash
python3 tests/ooxml_smoke.py tests/corpus/*.xlsx tests/corpus/*.xlsm
```

The smoke test verifies ZIP/OOXML structure and reports macro-bearing workbooks. It is not a substitute for visual/formula regression testing.
