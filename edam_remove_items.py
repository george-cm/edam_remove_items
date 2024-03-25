"""Removes items assinged to edam assets. Takes a CSV file with SKUs to remove
and removes the items from the edam export.
Outputs the updated data in a CSV file to import in eDAM.
"""
import csv
from pathlib import Path
import argparse
from typing import Literal


def main() -> None:
    """Main function."""
    parser = argparse.ArgumentParser(
        prog="edam_remove_items", description="Removes items assinged to edam assets."
    )
    parser.add_argument(
        "edam_export_file", type=str, help="Path to the edam export CSV file."
    )
    parser.add_argument(
        "skus_to_remove_file",
        type=str,
        help="Path to the CSV file containing a column named 'Item no.' "
        "with the items to remove.",
    )
    default_output_file = "edam_assets_with_removed_items.csv"
    parser.add_argument(
        "--output_file",
        type=str,
        help=f"Path to the output CSV file. Default: '{default_output_file}'",
        default=default_output_file,
    )

    args = parser.parse_args()

    edam_export_file = Path(args.edam_export_file)
    if not edam_export_file.exists():
        raise SystemExit(f"File {edam_export_file.as_posix()} does not exist.")

    skus_to_remove_file = Path(args.skus_to_remove_file)
    if not skus_to_remove_file.exists():
        raise SystemExit(f"File {skus_to_remove_file.as_posix()} does not exist.")

    output_file = Path(args.output_file)
    if not output_file.parent.exists():
        raise SystemExit(f"Directory {output_file.parent.as_posix()} does not exist.")

    edam_export_file_encoding: Literal["utf-8-sig"] | Literal["utf-8"] = (
        "utf-8-sig" if encoding_is_utf8_bom(edam_export_file) else "utf-8"
    )
    skus_to_remove_file_encoding: Literal["utf-8-sig"] | Literal["utf-8"] = (
        "utf-8-sig" if encoding_is_utf8_bom(skus_to_remove_file) else "utf-8"
    )

    skus_to_remove = set()
    with skus_to_remove_file.open("r", encoding=skus_to_remove_file_encoding) as f:
        reader = csv.DictReader(f)
        for row in reader:
            skus_to_remove.add(row["Item no."].strip())

    print(f"Removing {len(skus_to_remove)} items.")

    cols_to_update: list[str] = [
        "edam:item-to-pim{{String: multi }}",
        "edam:item-to-pim1{{String: multi }}",
        "edam:item-to-pim2{{String: multi }}",
        "edam:item-to-pim3{{String: multi }}",
    ]

    with edam_export_file.open(
        "r", encoding=edam_export_file_encoding
    ) as f, output_file.open("w", encoding="utf-8", newline="") as out:
        reader = csv.DictReader(f)
        writer = csv.DictWriter(out, fieldnames=reader.fieldnames)  # type: ignore
        writer.writeheader()
        cells_with_dropped_skus = 0
        rows_with_cells_with_dropped_skus = 0
        edam_row_count = 0
        for edam_row_count, row in enumerate(reader, start=1):
            skus_found_in_current_row: bool = False
            for column in cols_to_update:
                original_skus: list[str] = [x.strip() for x in row[column].split("|")]
                updated_skus: list[str] = [
                    x for x in original_skus if x not in skus_to_remove
                ]
                found_skus_to_drop: bool = len(original_skus) - len(updated_skus) > 0
                if found_skus_to_drop:
                    if not skus_found_in_current_row:
                        skus_found_in_current_row = True
                    cells_with_dropped_skus += 1
                    row[column] = "|".join(updated_skus)
            if skus_found_in_current_row:
                rows_with_cells_with_dropped_skus += 1
                writer.writerow(row)
        print(
            f"Found {cells_with_dropped_skus} cells with SKUs to remove"
            f"in {rows_with_cells_with_dropped_skus} rows\n"
            f"out of a total of {edam_row_count} rows in the edam export file."
        )


def encoding_is_utf8_bom(filepath: Path) -> bool:
    """Checks if a file is utf-8-bom encoded."""
    with filepath.open("rb") as f:
        return f.read(3) == b"\xef\xbb\xbf"


if __name__ == "__main__":
    main()
