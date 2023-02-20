import sys

if len(sys.argv) < 3:
    print("Usage: python update_html.py <user_pool_id> <app_client_id>")
    sys.exit(1)

user_pool_id = sys.argv[1]
app_client_id = sys.argv[2]
file_path = 'web\index.html'

with open(file_path, 'r') as file:
    data = file.read()

data = data.replace('<user-pool-id>', user_pool_id)
data = data.replace('<app-client-id>', app_client_id)

with open('web\index.html', 'w') as file:
    file.write(data)

print('Updated index.html with user pool ID {} and app client ID {}'.format(
    user_pool_id, app_client_id))

