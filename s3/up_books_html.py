import sys

file_path = 'web\\books.html'

# Check that the correct number of arguments were provided
if len(sys.argv) != 2:
    print("Usage: python update_html.py <api_gw_url>")
    sys.exit(1)

# Get the file path and API Gateway URL from the command-line arguments
api_gw_url = sys.argv[1]

# Read the contents of the file
with open(file_path, 'r') as file:
    content = file.read()

# Replace the placeholder with the API Gateway URL
content = content.replace('<api_gw_url>', api_gw_url)

# Write the updated content back to the file
with open(file_path, 'w') as file:
    file.write(content)

print(f"Successfully updated {file_path} with API Gateway URL: {api_gw_url}")
