import base64
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# OpenAI API Key
api_key = os.getenv("API_KEY")


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def get_list_of_items(image_path: Path, detail: str = "low"):
    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
                        You are given an image of groceries. 
                        Please create a list of all items included in the image and output only a JSON of the list. 
                        Nothing else but the JSON. The JSON should have one key called "groceries" and the list of items. 
                        
                        Example JSON:
                        ´´´
                        {
                            "groceries": [
                                "Apples",
                                "Bananas",
                                "Baby carrots",
                                "2% milk",
                                "Whole wheat bread",
                                "Organic eggs",
                                "Greek yogurt"
                            ]
                        }
                        ´´´
                        """,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": f"{detail if detail in ['low', 'high'] else 'low'}",
                        },
                    },
                ],
            }
        ],
        "max_tokens": 500,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )

    print(response.json())


def download_example_image(image_path: Path):
    if not image_path.exists():
        # The URL of the file you want to download
        file_url = "https://foto.wuestenigel.com/wp-content/uploads/api/gesunder-einkaufswagen-mit-veganen-lebensmitteln-frischem-obst-gemuse-und-kokosmilch.jpeg"

        # The local path where you want to save the downloaded file
        image_path.parent.mkdir(parents=True, exist_ok=True)

        # Perform the GET request
        response = requests.get(file_url, stream=True)

        # Open the local file in write-binary mode
        with open(image_path, "wb") as file:
            # Write the content of the response (the file's contents) to the local file
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    file.write(chunk)
        print(
            f"The example image of the groceries has been downloaded and saved to your local path"
            f"\n'{image_path.resolve()}'."
        )


if __name__ == "__main__":
    path = Path("images/groceries.jpg")

    download_example_image(path)

    get_list_of_items(path)
