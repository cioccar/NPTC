# Email Template (simplified version to match the screenshot exactly)
email_template = """Hello team,

This email is to inform you about NPT hours that can be taken by DE associates for Seller, Brand and Vendor business units.

This will help improve our occupancy rate, which has been below the YTD target for the last 4 weeks, as shown below:

                Week 32   Week 33   Week 34   Week 35
Actual Occupancy %   67.5%     67.8%     66.2%     66.7%
YTD Goal %          78.5%     78.5%     78.5%     78.5%

In the table below, you have the available hours divided by weeks and Staff Groups:

{table_placeholder}

To request NPT, you can use the River link for NPT requests.

Note: Requests may be denied if we notice that the requested interval does not meet minimum coverage requirements.

Thank you for your support!

Best Regards,
EMEA WFM"""

# Function to format the table for email (if needed)
def format_table_for_email(df):
    # Create a clean string representation of the table
    table_rows = []
    
    # Add headers
    headers = [str(col) for col in df.columns]
    table_rows.append("    ".join(headers))
    
    # Add separator
    table_rows.append("-" * (len("    ".join(headers))))
    
    # Add data rows
    for _, row in df.iterrows():
        formatted_row = [f"{str(val):>8}" for val in row]
        table_rows.append("    ".join(formatted_row))
    
    return "\n".join(table_rows)
