link: https://www.gradio.app/guides/quickstart


gr.interface has three core classes

fn: the function to wrap a user interface (UI) around
inputs: the Gradio component(s) to use for the input. The number of components should match the number of arguments in your function.
outputs: the Gradio component(s) to use for the output. The number of components should match the number of return values from your function.

