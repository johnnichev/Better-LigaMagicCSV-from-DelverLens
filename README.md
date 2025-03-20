# LigaMagic CSV Converter

## Overview
This project converts card inventory CSV files into the format required by **LigaMagic** for bulk imports.

## Features
- Reads `.csv` files from the `input_data` folder
- Converts them to LigaMagic’s required format
- Saves the output files in the `output_data` folder
- Supports language mapping (EN, BR, JP, ES, etc.)
- Automatically marks **Foil** and **Promo** cards

## Project Structure
```
.
├── input_data/          # Place input CSV files here
│   ├── .gitkeep
├── output_data/         # Converted files will be saved here
│   ├── .gitkeep
├── requirements/        # Stores dependencies
│   ├── requirements.txt
├── venv/                # Python virtual environment
├── convert_to_ligamagic.py  # The main script
├── README.md            # Project documentation
```

## Installation & Setup
### 1. Clone the Repository
```bash
git clone <repo-url>
cd <repo-name>
```

### 2. Create a Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment
```bash
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements/requirements.txt
```

## Usage
### 1. Add CSV files to `input_data`
Place all `.csv` files that need to be converted inside `input_data/`.

### 2. Run the Converter Script
```bash
python convert_to_ligamagic.py
```
This will process all CSV files in `input_data/` and generate the converted versions in `output_data/`.

### 3. Find Converted Files
The output files will be saved in `output_data/`.

## Example
### Input CSV Format (inside `input_data/`)
| Name                 | Edition          | Collector's number | Foil | Tag   | Language  | Condition        | Edition CODE | Quantity |
|----------------------|-----------------|--------------------|------|-------|-----------|-----------------|--------------|----------|
| Archpriest of Iona  | Zendikar Rising  | 5                  |      | Promo | Portuguese | Near Mint       | ZNR          | 1        |
| Confounding Conundrum | Zendikar Rising | 53                 |      |       | Portuguese | Near Mint       | ZNR          | 2        |

### Output CSV Format (inside `output_data/`)
| Edicao (Sigla) | Card (EN)              | Quantidade | Qualidade (M NM SP MP HP D) | Idioma (BR EN DE ES FR IT JP KO RU TW) | Card # | Extras  |
|---------------|-----------------------|-----------|----------------------------|---------------------------------|--------|--------|
| ZNR          | Archpriest of Iona      | 1         | NM                         | BR                              | 5      | Promo  |
| ZNR          | Confounding Conundrum   | 2         | NM                         | BR                              | 53     |        |

## Notes
- Ensure your input files have the correct format (Edition, Card Name, Condition, etc.).
- If a conversion error occurs, check the console output for details.

## Contributing
Feel free to fork this repository and submit pull requests!

## License
This project is licensed under the MIT License.

