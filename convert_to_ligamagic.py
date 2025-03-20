import pandas as pd
import os

def map_condition(condition):
    condition_map = {
        "Near Mint": "NM",
        "Slightly Played": "SP",
        "Moderately Played": "MP",
        "Heavily Played": "HP",
    }
    return condition_map.get(condition, "")

def map_language(language):
    language_map = {
        "Portuguese": "BR",
        "English": "EN",
        "Japanese": "JP",
        "Spanish": "ES",
        "German": "DE",
        "French": "FR",
        "Italian": "IT",
        "Korean": "KO",
        "Russian": "RU",
        "Traditional Chinese": "TW"
    }
    return language_map.get(language, "")

def map_edition(edition_code):
    edition_map = {
        "BRR": "rfbro",
        "GK2": "gk2o",
        "PLG21": "pwelb",
    }
    
    # Handle F16 and similar editions dynamically
    if edition_code.startswith("F") and edition_code[1:].isdigit():
        return "fnmp"
    
    return edition_map.get(edition_code, edition_code)  # Default to original if not mapped

def define_extras(foil, tag, collector_number):
    return {
        "Foil": 1 if pd.notna(foil) else 0,
        "Pre Release": 1 if pd.notna(tag) and "Pre Release" in tag else 0,
        "Promo": 1 if pd.notna(tag) and "Promo" in tag or str(collector_number).endswith("p") else 0,
    }

def convert_csv(input_file, output_file):
    # Load the input CSV file, skipping the first 4 rows (instructions)
    try:
        df = pd.read_csv(input_file, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, encoding="ISO-8859-1")
    
    # Trim column names to avoid space-related issues
    df.columns = df.columns.str.strip()
    
    # Print available columns to debug missing ones
    print("Available columns in input file:", df.columns.tolist())
    
    # Create a new DataFrame for the LigaMagic format
    df_converted = pd.DataFrame()
    
    # Define all required headers, ensuring they match LigaMagic's format
    df_converted["Tipo"] = "1"
    df_converted["Edição ID"] = ""
    df_converted["Edição Sigla"] = df.get("Edition CODE", "").apply(map_edition)
    df_converted["Carta ID"] = ""
    df_converted["Número"] = df.get("Collector's number", "")
    df_converted["Edição"] = df.get("Edition", "")
    df_converted["Raridade"] = ""
    df_converted["Cor"] = ""
    df_converted["Nome da Carta PT"] = ""
    df_converted["Nome da Carta EN"] = df.get("Name", "")
    df_converted["Idioma"] = df.get("Language", "").apply(map_language)
    df_converted["Qualidade"] = df.get("Condition", "").apply(map_condition)
    df_converted["Quantidade Existente"] = ""
    df_converted["Quantidade Para Somar/Subtrair"] = df.get("Quantity", "")
    df_converted["Preço"] = 0
    
    # Define extras (binary fields for LigaMagic format)
    extras = df.apply(lambda row: define_extras(
        row.get("Foil", ""),
        row.get("Tag", ""),
        row.get("Collector's number", "")
    ), axis=1)
    
    df_converted["Foil"] = [extra["Foil"] for extra in extras]
    df_converted["Foil Especial / Foil Etched"] = 0
    df_converted["Alterada"] = 0
    df_converted["Assinada"] = 0
    df_converted["Buy A Box"] = 0
    df_converted["DCI"] = 0
    df_converted["FNM"] = 0
    df_converted["Oversize"] = 0
    df_converted["Pre Release"] = [extra["Pre Release"] for extra in extras]
    df_converted["Promo"] = [extra["Promo"] for extra in extras]
    df_converted["Textless"] = 0
    df_converted["Misprint"] = 0
    df_converted["Miscut"] = 0
    
    # Save the converted file as CSV
    os.makedirs("output_data", exist_ok=True)
    output_path = os.path.join("output_data", output_file.replace(".xls", ".csv"))
    df_converted.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"Converted file saved to: {output_path}")

if __name__ == "__main__":
    input_folder = "input_data"
    output_folder = "output_data"
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    
    input_files = [f for f in os.listdir(input_folder) if f.endswith(".csv")]
    
    if not input_files:
        print("No CSV files found in input_data folder.")
    else:
        for input_file in input_files:
            output_file = f"converted_{input_file}"
            convert_csv(os.path.join(input_folder, input_file), output_file)
