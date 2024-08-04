import cv2
import numpy as np
import pyautogui
import base64
import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
# Global variables for text properties
TEXT_SCALE = 1
TEXT_THICKNESS = 4
def capture_screenshot():
    from PIL import ImageGrab
    #screenshot = ImageGrab.grab(all_screens=True)
    #screenshot = ImageGrab.grab([1920, 0, 1920 * 2, 1080], all_screens=True)
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
def draw_grid(image, grid_size=100):
    height, width = image.shape[:2]
    # Draw vertical lines
    for x in range(0, width, grid_size):
        cv2.line(image, (x, 0), (x, height), (0, 255, 0), 1)
        # Add X coordinate at the top
        #cv2.putText(image, str(x), (x, 30), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE, (0, 0, 255), TEXT_THICKNESS)
        # Add X coordinate at the bottom
        cv2.putText(image, str(x), (x, height - 10), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE, (0, 0, 255), TEXT_THICKNESS)
        # meio
        #cv2.putText(image, str(x), (x + 20, height // 2), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE, (0, 0, 255), TEXT_THICKNESS)
    # Draw horizontal lines
    for y in range(0, height, grid_size):
        cv2.line(image, (0, y), (width, y), (0, 255, 0), 1)
        # Add Y coordinate on the left (increasing from bottom to top)
        cv2.putText(image, str(height - y + 2), (5, y), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE, (0, 0, 255), TEXT_THICKNESS)
        # Add Y coordinate on the right (increasing from bottom to top)
        #cv2.putText(image, str(height - y + 2), (width - 100, y), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE, (0, 0, 255), TEXT_THICKNESS)
        # meio
        #cv2.putText(image, str(height - y), (width // 2 - 30, y - 10), cv2.FONT_HERSHEY_SIMPLEX, TEXT_SCALE, (0, 0, 255), TEXT_THICKNESS)
    return image
def resize_image(image, scale_percent=75):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    return cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

def encode_image_to_base64(image):
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

def ask_gpt4_coordinates(pergunta, image):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return None

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        #"model": "gpt-4-vision-preview",
        #"model": "gpt-4o",
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                
                "content": [
                    {
                        "type": "text",
                        "text": f"""A imagem tem as coordenadas do eixo X e Y. Responda com um JSON informando X e Y. Qual a coordenada {pergunta}?
                        Caso não encontre, responda a coordenada 0,0""",
                        "response_format": { "type": "json_object" }
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{encode_image_to_base64(image)}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    
    if response.status_code == 200:
        text = response.json()["choices"][0]["message"]["content"].lower()
        print(text)
        start = text.find('```json')
        end = text.find('```', start + 1)
        json_text = text[start+7:end]
        #text = text.strip("```").strip("json")
        if start == -1:
            data = {"x": 0, "y" : 0}
        else:
            data = json.loads(json_text)
        return data
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def draw_cursor_position(image):
    x, y = pyautogui.position()
    height, width = image.shape[:2]
    y_adjusted = height - y
    cv2.ellipse(image, (x, y_adjusted), (15, 15), 0, 0, 360, (0, 0, 0), 6)
    cv2.ellipse(image, (x, y_adjusted), (15, 15), 0, 0, 360, (255, 255, 255), 2)
    cv2.putText(image, f"({x}, {y})", (x + 20, y_adjusted), cv2.FONT_HERSHEY_SIMPLEX, 
                TEXT_SCALE, (0, 0, 0), TEXT_THICKNESS + 4)
    cv2.putText(image, f"({x}, {y})", (x + 20, y_adjusted), cv2.FONT_HERSHEY_SIMPLEX, 
                TEXT_SCALE, (255, 255, 255), TEXT_THICKNESS)
    return image
def main():
    iter = 0;
    while iter == 0:
        iter+= 1
        screenshot = capture_screenshot()
        grid_image = draw_grid(screenshot.copy())
    
        coordenada = ask_gpt4_coordinates("do texto do botão 'send'", grid_image)
        print(coordenada)
        pyautogui.moveTo(coordenada['x'], coordenada['y'])

        # Draw cursor position
        grid_image = draw_cursor_position(grid_image)

        # Resize the image to 3/4 of its original size
        resized_image = resize_image(grid_image, scale_percent=75)

        cv2.imshow("Screenshot with Grid and Cursor (3/4 size)", resized_image)
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
