# This scripts reads .hej files containing genealogic data and converts them to csv. 4 csvs are generated personen, mrg, ortv, quellv. 'adop' seems to be another potential part of these files, but no data was included in the investigates .hej file, so no conclusions/conversions can be made for now.

import csv
import re
import os



# Data folder where input and output files are located
data_folder = 'c:/choose/your/folder'

# Filename containing the raw data
data_file = os.path.join(data_folder, "filename.hej")

# Define control characters
field_delimiter = '\x0f'  # Corresponds to character ''
note_delimiter = '\x10'   # Corresponds to character ''

# Lists to store the records
personen_data = []
mrg_data = []
ortv_data = []
quellv_data = []

# Current record type
current_type = 'personen'

# Open the file and read it line by line
with open(data_file, 'r', encoding='cp1252') as file:
    for line in file:
        line = line.strip()
        if not line:
            continue  # Skip empty lines

        # Check for section change
        if line == 'mrg':
            current_type = 'mrg'
            continue
        elif line == 'ortv':
            current_type = 'ortv'
            continue
        elif line == 'quellv':
            current_type = 'quellv'
            continue

        # Process data according to the current type
        if current_type == 'personen':
            # Extract notes and replace them with a placeholder
            notes = re.findall(f'{note_delimiter}(.*?){note_delimiter}', line)
            line_without_notes = re.sub(f'{note_delimiter}.*?{note_delimiter}', '<<NOTE>>', line)

            # Split the record into fields
            fields = line_without_notes.split(field_delimiter)

            # Replace the placeholder with empty strings in fields
            fields = [field.replace('<<NOTE>>', '') for field in fields]

            # Add notes at the correct position if available
            if notes:
                kommentar = ' '.join(notes)
            else:
                kommentar = ''

            # Ensure the number of fields matches the header
            while len(fields) < 49:  # Adjust the number as per your header
                fields.append('')

            # Insert the 'Kommentar' field at the correct index (31)
            fields[31] = kommentar

            # Append only the required number of fields
            personen_data.append(fields[:49])

        elif current_type == 'mrg':
            fields = line.split(field_delimiter)
            mrg_data.append(fields)
        elif current_type == 'ortv':
            fields = line.split(field_delimiter)
            ortv_data.append(fields)
        elif current_type == 'quellv':
            fields = line.split(field_delimiter)
            quellv_data.append(fields)

# Header fields for the CSV files (keep in German)
personen_header = [
    'Datensatz_ID', 'Vater_ID', 'Mutter_ID', 'Nachname', 'Vorname', 'Geschlecht', 'Religion', 'Beruf',
    'Geburts_Tag', 'Geburts_Monat', 'Geburts_Jahr', 'Geburtsort', 'Unbekannt1', 'Unbekannt2', 'Unbekannt3',
    'Unbekannt4', 'Unbekannt5', 'Wohnort', 'Sterbe_Tag', 'Sterbe_Monat', 'Sterbe_Jahr', 'Sterbeort',
    'Todesursache', 'Unbekannt6', 'Unbekannt7', 'Unbekannt8', 'Unbekannt9', 'Unbekannt10', 'Unbekannt11',
    'Unbekannt12', 'Unbekannt13', 'Kommentar', 'Unbekannt14', 'Unbekannt15', 'Unbekannt16', 'Unbekannt17',
    'Spitznamen', 'Unbekannt18', 'Unbekannt19', 'Unbekannt20', 'Unbekannt21', 'Unbekannt22', 'Unbekannt23',
    'Unbekannt24', 'Unbekannt25', 'Unbekannt26', '', '', ''
]

# Ensure the number of headers matches the number of fields
assert len(personen_header) == 49, "The number of header fields does not match the number of data fields."

mrg_header = [
    'Person1_ID', 'Person2_ID', 'Heirats_Tag', 'Heirats_Monat', 'Heirats_Jahr', 'Heiratsort',
    'Feld7', 'Feld8', 'Feld9', 'Feld10', 'Feld11', 'Feld12', 'Ereignisart', 'Feld14', 'Feld15',
    'Feld16', 'Feld17', 'Feld18', 'Feld19', 'Feld20'
]

ortv_header = [
    'Ortsname', 'Feld2', 'Feld3', 'Feld4', 'Feld5', 'Feld6', 'Feld7', 'Feld8', 'Feld9', 'Feld10', 'Feld11'
]

quellv_header = [
    'Quellen_ID', 'Feld2', 'Feld3', 'Feld4', 'Feld5', 'Feld6', 'Feld7', 'Feld8', 'Feld9', 'Feld10'
]

# Function to write data to CSV files
def write_csv(filename, header, data):
    filepath = os.path.join(data_folder, filename)
    with open(filepath, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(header)
        for row in data:
            # If the row has fewer fields than the header, fill with empty strings
            if len(row) < len(header):
                row.extend([''] * (len(header) - len(row)))
            writer.writerow(row)

# Save CSV files
write_csv('personen.csv', personen_header, personen_data)
write_csv('mrg.csv', mrg_header, mrg_data)
write_csv('ortv.csv', ortv_header, ortv_data)
write_csv('quellv.csv', quellv_header, quellv_data)

print("Data has been successfully converted to CSV files.")
