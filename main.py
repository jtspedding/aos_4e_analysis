
import os
import re # reg expression

import pandas as pd

from dotenv import load_dotenv, find_dotenv, dotenv_values
from pdfminer.high_level import extract_pages, extract_text
from bs4 import BeautifulSoup

load_dotenv(dotenv_path=find_dotenv(),verbose=True) # set env variable.

#for page_layout in extract_pages("/Warscroll_index/2024-07-14 Hedonites of Slaanesh Index.pdf"):

text_raw = extract_text("Warscroll_index/2024-07-14 Hedonites of Slaanesh Index.pdf")
#text_raw = extract_text("Warscroll_index/2024-08-03 Kharadron Overlords Index.pdf")

matches = pattern.findall(text_raw)

len(matches) # num of warscrolls (incl spearhead).
#print(matches)

print(text_raw)

# NOT WORKING:
#parsed = [x.split("HEDONITES OF SLAANESH WARSCROLL") for x in text.split("HEDONITES OF SLAANESH WARSCROLL")]
#parsed
#pattern = re.compile(r"HEDONITES OF SLAANESH WARSCROLL")


# BELOW: function to grab everything after "HEDONITES OF SLAANESH WARSCROLL" and assign it to element in "text"
def parse_raw_text(text, faction_specific_regex):
    # https://stackoverflow.com/questions/74395149/using-python-to-parse-plain-text-messages-that-use-and-as-delimiters
    
    # create a list of all the records, separated by "HEDONITES OF SLAANESH WARSCROLL"/faction_specific_regex.
    raw_records = text.split(faction_specific_regex)

    records = []
    for record in raw_records:
        # if there is no data in the record, skip it
        if not record:
            continue
        # split each record into parts, separated by "\n"
        records += [record.split("\n")]

    # replace all values of "-" with None
    for record in records:
        for i, value in enumerate(record):
            if value == "-":
                record[i] = None
    return records

df_warscrolls = parse_raw_text(text_raw, "HEDONITES OF SLAANESH WARSCROLL") # 

df_warscrolls.shape

df_warscrolls[1] #Shalaxi helbane
df_warscrolls[2] #Keeper
df_warscrolls[10] #Hellflayer

raw_text = [df_warscrolls[5],
            df_warscrolls[1],
            df_warscrolls[2]
 ]

print(raw_text)
type(raw_text)


###################################################################################
# Below was written by copilot, kinda almost worked but didn't.
# "write code to extract raw_text (above) and save it to a df likebelow..."

#ws_name	MELEE WEAPONS	Atk	Hit	Wnd	Rnd	Dmg
#SYLL'ESSKE	Axe of Dominion	4	3+	3+	2	3
#SYLL'ESSKE	Scourging Whip	6	2+	4+	1	2
#SHALAXI HELBANE	Soulpiercer	6	2+	3+	2	3
#SHALAXI HELBANE	Impaling Claws	2	3+	3+	2	4
#KEEPER OF SECRETS	Elegant Greatblade	6	2+	3+	2	2
#KEEPER OF SECRETS	Impaling Claws	2	3+	3+	2	4

# Initialize a list to store each dataframe rows
df_rows = []

# We iterate over each page
for page in pages:
    page_soup = soup(page, "lxml")

    # Here we get only the <a> tag inside the tbody and each tr
    # We avoid getting the links from the head of the table
    all_links = page_soup.select("tbody tr a")
    # We extract the href for only the links containing council (we don't care about the
    # video link)
    minutes_links = [x.attrs["href"] for x in all_links if "council" in x.attrs["href"]]

    #
    for link in minutes_links:
        pdf_name, pages_text = get_pdf(link)

        df_rows.append(
            {
                "PDF_file_name": pdf_name,
                # We join each page in the list into one string, separting them with a line return
                "PDF_text": "\n".join(pages_text),
            }
        )

        break
    break

# We create the data frame from the list of rows
df = pd.DataFrame(df_rows)













# Extract relevant data
data = []
for entry in raw_text:
    ws_name = entry[2]
    weapons = entry[7:9]
    stats = entry[11:17]
    for i, weapon in enumerate(weapons):
        data.append([ws_name, weapon] + stats[i*3:(i+1)*3])

# Create dataframe
df = pd.DataFrame(data, columns=['ws_name', 'MELEE WEAPONS', 'Atk', 'Hit', 'Wnd', 'Rnd', 'Dmg'])

# Display dataframe
print(df)



raw_text = [[' •', '', 'SYLL’ESSKE', '', 'THE VENGEFUL ALLEGIANCE', '', 'MELEE WEAPONS', 'Axe of Dominion', 'Scourging Whip', '', 'Atk Hit Wnd Rnd Dmg', '3+ 3+ 2', '4', '2+ 4+ 1', '6', '', '3', '2', ''], 
            [' •', '', 'SHALAXI HELBANE', '', 'MELEE WEAPONS', '', 'Soulpiercer', 'Impaling Claws', '', 'Atk Hit Wnd Rnd Dmg', '2+ 3+ 2', '6', '3+ 3+ 2', '2', '', '3', '4', ''], 
            [' •', '', 'KEEPER OF SECRETS', '', 'MELEE WEAPONS', 'Elegant Greatblade', 'Impaling Claws', '', 'Atk Hit Wnd Rnd Dmg', '2+ 3+ 2', '6', '3+ 3+ 2', '2', '', '2', '4', '']]

# Extract relevant data
data = []
for entry in raw_text:
    ws_name = entry[2]
    weapons = entry[7:9]
    stats = entry[11:17]
    for i, weapon in enumerate(weapons):
        atk, hit, wnd = stats[i*3].split()
        rnd = stats[i*3 + 1]
        dmg = stats[i*3 + 2]
        data.append([ws_name, weapon, atk, hit, wnd, rnd, dmg])

# Create dataframe
df = pd.DataFrame(data, columns=['ws_name', 'MELEE WEAPONS', 'Atk', 'Hit', 'Wnd', 'Rnd', 'Dmg'])






# ctrl shift P



import pandas as pd

# Raw text data
raw_text = [[' •', '', 'SYLL’ESSKE', '', 'THE VENGEFUL ALLEGIANCE', '', 'MELEE WEAPONS', 'Axe of Dominion', 'Scourging Whip', '', 'Atk Hit Wnd Rnd Dmg', '3+ 3+ 2', '4', '2+ 4+ 1', '6', '', '3', '2', ''], 
            [' •', '', 'SHALAXI HELBANE', '', 'MELEE WEAPONS', '', 'Soulpiercer', 'Impaling Claws', '', 'Atk Hit Wnd Rnd Dmg', '2+ 3+ 2', '6', '3+ 3+ 2', '2', '', '3', '4', ''], 
            [' •', '', 'KEEPER OF SECRETS', '', 'MELEE WEAPONS', 'Elegant Greatblade', 'Impaling Claws', '', 'Atk Hit Wnd Rnd Dmg', '2+ 3+ 2', '6', '3+ 3+ 2', '2', '', '2', '4', '']]

# Extract relevant data
data = []
for entry in raw_text:
    ws_name = entry[2]
    weapons = entry[7:9]
    stats = entry[11:17]
    for i, weapon in enumerate(weapons):
        atk, hit, wnd = stats[i*2].split()
        rnd = stats[i*2 + 1]
        dmg = stats[i*2 + 2]
        data.append([ws_name, weapon, atk, hit, wnd, rnd, dmg])

# Create dataframe
df = pd.DataFrame(data, columns=['ws_name', 'MELEE WEAPONS', 'Atk', 'Hit', 'Wnd', 'Rnd', 'Dmg'])

# Display dataframe
print(df)




df.shape

df.iloc[2]

from IPython.display import display
display(df)

df.style

print(df)