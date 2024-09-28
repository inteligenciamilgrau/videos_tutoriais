
import gradio as gr
from huggingface_hub import InferenceClient

"""
For more information on `huggingface_hub` Inference API support, please check the docs: https://huggingface.co/docs/huggingface_hub/v0.22.2/en/guides/inference
"""
client = InferenceClient("HuggingFaceH4/zephyr-7b-beta")
#client = InferenceClient("unsloth/Llama-3.2-1B-Instruct")


def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""


    try:
        for message in client.chat_completion(
            messages,
            max_tokens=max_tokens,
            stream=True,
            temperature=temperature,
            top_p=top_p,
        ):
            # Ensure the message has a valid structure
            if not message or not isinstance(message, dict):
                continue
            
            try:
                # Extract content and finish reason
                content = message.choices[0].delta.content
                finish_reason = message.choices[0].finish_reason

                # Check if the content is empty
                if content.strip() == "":
                    # If the finish reason is 'stop', it's expected and we can break the loop
                    if finish_reason == "stop":
                        print("Stream ended normally.")
                        break
                    else:
                        print("Received unexpected empty content, skipping...")
                        continue

                response += content
                yield response

            except (AttributeError, IndexError, KeyError) as e:
                print(f"Error processing message: {e}")
                continue

    except Exception as e:
        print(f"Unexpected error: {e}")
        yield "An error occurred while generating the response."

    # Final check if the response is empty
    if response.strip() == "":
        yield "No response generated. Please try again or adjust the settings."


"""
For information on how to customize the ChatInterface, peruse the gradio docs: https://www.gradio.app/docs/chatinterface
"""
demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value="You are a friendly Chatbot. Your name is Juninho.", label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
)


if __name__ == "__main__":
    demo.launch()
