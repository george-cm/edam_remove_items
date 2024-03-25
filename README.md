# edam_remove_items

Removes items assinged to eDAM assets.
Takes a CSV file with SKUs to remove and removes the items from the edam export.
Outputs the updated data in a CSV file to import in eDAM.

## Usage

```console
edam_remove_items [-h] [--output_file OUTPUT_FILE] edam_export_file skus_to_remove_file

Removes items assinged to edam assets.

positional arguments:
  edam_export_file      Path to the edam export CSV file.
  skus_to_remove_file   Path to the CSV file containing a column named 'Item no.' with the items to remove.

options:
  -h, --help            show this help message and exit
  --output_file OUTPUT_FILE
                        Path to the output CSV file. Default: 'edam_assets_with_removed_items.csv'
```

## Examples

On windows:

```console
python .\edam_remove_items.py '.\SpareParts_21.03.2024.csv' '.\SKUs needs to remove.csv'
```

On \*nix:

```console
python ./edam_remove_items.py './SpareParts_21.03.2024.csv' './SKUs needs to remove.csv'
```

## Requirements

Python 3.11+

## License

MIT
