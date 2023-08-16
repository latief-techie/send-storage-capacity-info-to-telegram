import os
import psutil
import requests
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
bot_token = os.environ.get("BOT_TOKEN")
user_id = os.environ.get("CHAT_ID")

def get_remaining_storage(path='/'):
    try:
        usage = psutil.disk_usage(path)
        remaining = usage.free
        return remaining
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_remaining_storage_total(path='/'):
    try:
        usage = psutil.disk_usage(path)
        total = usage.total
        return total
    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    storage_path = "/"  # You can specify the path to the specific disk/partition if needed
    remaining_storage = get_remaining_storage(storage_path)
    remaining_percent = (remaining_storage / get_remaining_storage_total(storage_path)) * 100

    if remaining_storage is not None:
        server = "Wifinetbill server"
        mega_byte = f"Remaining storage on {storage_path}: {remaining_storage / (1024 * 1024)} MB"
        giga_byte = f"Remaining storage on {storage_path}: {remaining_storage / (1024**2):.2f} GB"
        percentage = f"Remaining storage on {storage_path}: {remaining_percent:.2f}%"
        message = f"{mega_byte}\n{giga_byte}\n{percentage}"
    else:
        server = "Wifinetbill server"
        messageError = "Failed to retrieve storage information."
        message = f"{server}\n{messageError}"

api_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
data = {
    'chat_id': user_id,
    'text': message
}

response = requests.post(api_url, data=data)

if response.status_code == 200:
    print("Message sent successfully.")
else:
    print("Failed to send the message. Status code:", response.status_code)
    print(response.text)
