
import gradio as gr

def my_tool(input_text: str) -> str:
    """Do something with input.

    Args:
        input_text: The input

    Returns:
        The result
    """
    return f"Processed: {input_text}"

demo = gr.Interface(
    fn=my_tool,
    inputs="text",
    outputs="text"
)

if __name__ == "__main__":
    demo.launch(mcp_server=True)
