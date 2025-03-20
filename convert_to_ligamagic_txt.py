import pandas as pd
import os

def define_extras(foil, tag, collector_number):
    return {
        "Foil": 1 if pd.notna(foil) else 0,
        "Pre Release": 1 if pd.notna(tag) and "Pre Release" in tag else 0,
        "Promo": 1 if pd.notna(tag) and "Promo" in tag or str(collector_number).endswith("p") else 0,
    }

def map_edition(edition_code, colors):
    # Handle F16 and similar editions dynamically
    if edition_code.startswith("F") and edition_code[1:].isdigit():
        return "FNMP"

    # Handle GuildKit editions
    # Handle GK1 guilds
    if edition_code == "GK1":
        if "Green" in colors and "White" in colors:  # Selesnya
            return "gk1s"
        elif "Red" in colors and "White" in colors:  # Boros
            return "gk1b"
        elif "Black" in colors and "Green" in colors:  # Golgari
            return "gk1g"
        elif "Blue" in colors and "Red" in colors:  # Izzet
            return "gk1i"
        elif "Blue" in colors and "Black" in colors:  # Dimir
            return "gk1d"

    # Handle GK2 guilds
    if edition_code == "GK2":
        if "Green" in colors and "Blue" in colors:  # Simic
            return "gk2s"
        elif "Black" in colors and "Red" in colors:  # Rakdos
            return "gk2r"
        elif "White" in colors and "Black" in colors:  # Orzhov
            return "gk2o"
        elif "Red" in colors and "Green" in colors:  # Gruul
            return "gk2g"
        elif "White" in colors and "Blue" in colors:  # Azorius
            return "gk2a"
    
    edition_map = {
        "BRR": "RFBRO",
        "PLG21": "PWELB",
        "PDOM": "DW1",
        "PW21": "PWP21",
        "PLST": "PLIST"
    }
    
    return edition_map.get(edition_code, edition_code)  # Default to original if not mapped

def format_txt_line(row):
    mapped_edition = map_edition(row['Edition CODE'], row['Color'])
    return f"{row['Quantity']} {row['Name']} [{mapped_edition}] ({row['Condition']}, {row['Language']})" + (f" {row['Price']}" if row['Price'] > 0 else " 0")

def convert_csv_to_txt(input_file):
    try:
        df = pd.read_csv(input_file, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, encoding="ISO-8859-1")
    
    df["Price"] = df.get("Price", 0)
    
    extras = df.apply(lambda row: define_extras(row.get("Foil"), row.get("Tag"), row.get("Collector's number")), axis=1)
    df["Foil"] = [extra["Foil"] for extra in extras]
    df["Pre Release"] = [extra["Pre Release"] for extra in extras]
    df["Promo"] = [extra["Promo"] for extra in extras]
    
    categories = {
        "only_foil": df[(df["Foil"] == 1) & (df["Pre Release"] == 0) & (df["Promo"] == 0)],
        "only_pre_release": df[(df["Pre Release"] == 1) & (df["Foil"] == 0) & (df["Promo"] == 0)],
        "only_promo": df[(df["Promo"] == 1) & (df["Foil"] == 0) & (df["Pre Release"] == 0)],
        "foil_and_promo": df[(df["Foil"] == 1) & (df["Promo"] == 1) & (df["Pre Release"] == 0)],
        "foil_and_pre_release": df[(df["Foil"] == 1) & (df["Pre Release"] == 1) & (df["Promo"] == 0)],
        "no_extras": df[(df["Foil"] == 0) & (df["Pre Release"] == 0) & (df["Promo"] == 0)]
    }
    
    os.makedirs("output_data", exist_ok=True)
    
    for category, data in categories.items():
        if not data.empty:
            output_path = os.path.join("output_data", f"{category}_{os.path.basename(input_file).replace('.csv', '.txt')}")
            with open(output_path, "w", encoding="utf-8") as txt_file:
                for _, row in data.iterrows():
                    txt_file.write(format_txt_line(row) + "\n")
            print(f"Saved: {output_path}")

if __name__ == "__main__":
    input_folder = "input_data"
    os.makedirs(input_folder, exist_ok=True)
    
    input_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    
    if not input_files:
        print("No CSV files found in input_data folder.")
    else:
        for input_file in input_files:
            convert_csv_to_txt(os.path.join(input_folder, input_file))
