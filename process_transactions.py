import pandas as pd
import getpass
from fuzzywuzzy import process

def main():
    # Grab the username of the system
    username = getpass.getuser()

    # Read in transaction data
    df = pd.read_csv(f"/Users/{username}/Desktop/{username} Documents/Credit card/12-May-2024.csv", header=None)

    # Rename columns
    df.columns = ["date", "value", "desc"]

    # List of suburb names in Sydney and Melbourne, Australia (you can replace this with a more comprehensive list)
    sydney_suburbs = [
        "SYDNEY", "BARANGAROO", "CAMPERDOWN", "NORTH STRATHFIELD", "SURRY HILLS",
        "BONDI", "SYDNEY OLYMPIC PARK", "RHODES", "NEWTOWN", "ENMORE", "CONCORD",
        "BURWOOD", "REDFERN", "ROZELLE", "MARRICKVILLE", "LIDCOMBE", "STRATHFIELD",
        "WEST RYDE", "EASTWOOD", "RYDE", "ALEXANDRIA", "HOMEBUSH"
    ]

    melbourne_suburbs = [
        "MELBOURNE", "SOUTH YARRA", "FITZROY", "RICHMOND", "BOX HILL", "HAWTHORN",
        "KEW", "DONCASTER", "NUNAWADING", "BALWYN", "BALWYN NORTH", "MENTONE", "MULGRAVE"
    ]

    def extract_location(text, suburbs):
        matches = process.extract(text, suburbs, limit=1)
        if matches and matches[0][1] >= 80:  # Set a threshold for the match score
            return matches[0][0]
        return "online"  # Return "online" if no match is found or the match score is below the threshold

    # Apply the extract_location function to the "desc" column for Sydney suburbs
    df["location"] = df["desc"].apply(lambda x: extract_location(x, sydney_suburbs + melbourne_suburbs))

    # Create a new column "is_sydney" and set it to 1 for rows containing a Sydney suburb, 0 otherwise
    df["is_sydney"] = df["location"].apply(lambda x: 1 if x in sydney_suburbs else 0)

    # Export the resulting data as CSV
    output_file = f"/Users/{username}/Desktop/{username} Documents/Credit card/output.csv"
    df.to_csv(output_file, index=False)

    print(f"Output CSV file saved as: {output_file}")

if __name__ == "__main__":
    main()