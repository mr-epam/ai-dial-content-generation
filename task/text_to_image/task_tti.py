import asyncio
from datetime import datetime

from task._models.custom_content import Attachment
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role

class Size:
    """
    The size of the generated image.
    """
    square: str = '1024x1024'
    height_rectangle: str = '1024x1792'
    width_rectangle: str = '1792x1024'


class Style:
    """
    The style of the generated image. Must be one of vivid or natural.
     - Vivid causes the model to lean towards generating hyper-real and dramatic images.
     - Natural causes the model to produce more natural, less hyper-real looking images.
    """
    natural: str = "natural"
    vivid: str = "vivid"


class Quality:
    """
    The quality of the image that will be generated.
     - ‘hd’ creates images with finer details and greater consistency across the image.
    """
    standard: str = "standard"
    hd: str = "hd"

async def _save_images(attachments: list[Attachment]):
    # TODO:
    #  1. Create DIAL bucket client
    #  2. Iterate through Images from attachments, download them and then save here
    #  3. Print confirmation that image has been saved locally

    ## raise NotImplementedError

    async with DialBucketClient(API_KEY, DIAL_URL) as bucket_client:
        for i, attachment in enumerate(attachments):
            if attachment.url:
                # Download the image from DIAL bucket
                image_bytes = await bucket_client.get_file(attachment.url)

                # Create a filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"generated_image_{timestamp}_{i}.png"

                # Save to local file
                with open(filename, "wb") as f:
                    f.write(image_bytes)

                print(f"Image saved: {filename}")

def start() -> None:
    # TODO:
    #  1. Create DialModelClient
    #  2. Generate image for "Sunny day on Bali"
    #  3. Get attachments from response and save generated message (use method `_save_images`)
    #  4. Try to configure the picture for output via `custom_fields` parameter.
    #    - Documentation: See `custom_fields`. https://dialx.ai/dial_api#operation/sendChatCompletionRequest
    #  5. Test it with the 'imagegeneration@005' (Google image generation model)

    ## raise NotImplementedError

    # 1. Create DialModelClient for image generation
    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="dall-e-3",  # or "imagegeneration@005" for Google
        api_key=API_KEY
    )

    # 2. Generate image with a text prompt
    message = Message(
        role=Role.USER,
        content="Sunny day on Bali"
    )

    # Optional: Configure with custom_fields for size, quality, style
    custom_fields = {
        "size": Size.square,
        "quality": Quality.hd,
        "style": Style.vivid
    }

    response = client.get_completion([message], custom_fields=custom_fields)

    # 3. Get attachments from response and save them
    if response.custom_content and response.custom_content.attachments:
        asyncio.run(_save_images(response.custom_content.attachments))
        print(f"Generated {len(response.custom_content.attachments)} image(s)")
    else:
        print("No images generated")

start()
