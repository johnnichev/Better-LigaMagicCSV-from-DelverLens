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
    extras = []
    if pd.notna(foil):
        extras.append("Foil")
    if pd.notna(tag):
        if "Promo" in tag:
            extras.append("Promo")
        if "Pre Release" in tag:
            extras.append("Pre Release")
    if str(collector_number).endswith("p"):
        extras.append("Promo")
    return ", ".join(extras) if extras else ""

def convert_csv(input_file, output_file):
    # Load the input CSV file
    try:
        df = pd.read_csv(input_file, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(input_file, encoding="ISO-8859-1")
    
    # Create a new DataFrame for the LigaMagic format
    df_converted = pd.DataFrame()
    
    
    # Leave edition names empty
    df_converted["Edicao (PTBR)"] = ""
    df_converted["Edicao (EN)"] = df["Edition"]
    
    # Map edition codes
    df_converted["Edicao (Sigla)"] = df["Edition CODE"].apply(map_edition)

    # Map card names
    df_converted["Card (PT)"] = ""
    df_converted["Card (EN)"] = df["Name"]
    
    # Map quantity
    df_converted["Quantidade"] = df["Quantity"]
    
    # Convert condition
    df_converted["Qualidade (M NM SP MP HP D)"] = df["Condition"].apply(map_condition)
    
    # Convert language
    df_converted["Idioma (BR EN DE ES FR IT JP KO RU TW)"] = df["Language"].apply(map_language)
    
    # Keep rarity and color empty
    df_converted["Raridade (M R U C)"] = ""
    df_converted["Cor (W U B R G M A L)"] = ""
    
    # Map collector's number
    df_converted["Card #"] = df["Collector's number"]
    
    # Define extras
    df_converted["Extras"] = df.apply(lambda row: define_extras(row["Foil"], row["Tag"], row["Collector's number"]), axis=1)
    
    # Add empty comment field
    df_converted["Comentario"] = ""
    
    # Save the converted file
    os.makedirs("output_data", exist_ok=True)
    output_path = os.path.join("output_data", output_file)
    df_converted.to_csv(output_path, index=False, encoding="utf-8")
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
