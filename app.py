import gradio as gr
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load your fine-tuned or pre-trained model
model_name = "google/flan-t5-small"  # Replace with your fine-tuned model name if applicable
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Function to generate JSON output
def generate_json(
    message,  # Input instruction
    max_tokens,
    temperature,
    top_p,
):
    inputs = tokenizer(message, return_tensors="pt", truncation=True, max_length=512)
    outputs = model.generate(
        inputs["input_ids"],
        max_length=128, # reduce max token to 128
        temperature=temperature,
        top_p=top_p,
        num_beams=3,  # Increase for more refined outputs
    )
    result = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return result

# Gradio interface
demo = gr.Interface(
    fn=generate_json,
    inputs=[
        gr.Textbox(value="", label="Input Instruction", placeholder="Enter instruction, e.g., Generate a JSON for a user named John Doe."),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p"),
    ],
    outputs="text",
    title="JSON Generator",
    description="Provide an instruction to generate JSON outputs for your domain.",
)

if __name__ == "__main__":
    demo.launch()