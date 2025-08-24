def explanation_prompt(topic, memory="", doc=""):
    return f"""
You are a helpful Python tutor.

Context from previous conversation:
{memory}

Context from uploaded document:
{doc}

Explain the following concept clearly, with one simple example:

Topic: {topic}
"""

def code_generation_prompt(task, memory="", doc=""):
    return f"""
You are a Python expert.

Context from previous conversation:
{memory}

Context from uploaded document:
{doc}

Write Python code to accomplish the following task:

Task: {task}
"""

def debug_prompt(code, memory="", doc=""):
    return f"""
You are a Python code debugger.

Context from previous conversation:
{memory}

Context from uploaded document:
{doc}

The user has written the following code:\n\n{code}

Identify any errors and provide a corrected version.
"""
