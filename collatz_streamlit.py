import streamlit as st
import numpy as np
import plotly.graph_objects as go

def collatz_step(n):
    """Perform a single step of the Collatz operation."""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def custom_step(n, op1, op2):
    """Perform a custom operation based on user-defined functions."""
    if n % 2 == 0:
        return eval(op1)
    else:
        return eval(op2)

def generate_sequence(n, steps=None, custom_ops=None):
    """Generate the sequence of numbers based on Collatz or custom operations."""
    sequence = [n]
    for _ in range(steps if steps else 10):  # Large default max steps
        if sequence[-1] == 1:
            break
        if custom_ops:
            next_num = custom_step(sequence[-1], custom_ops[0], custom_ops[1])
        else:
            next_num = collatz_step(sequence[-1])
        sequence.append(next_num)
    return sequence

### MAIN ###
st.title("Collatz Conjecture Explorer")

# User Inputs
st.sidebar.header("Settings")
number = st.sidebar.number_input("Starting Number", min_value=-1000, value=7, step=1)
max_steps = st.sidebar.number_input("Max Steps (0 for full sequence to 1)", min_value=0, value=0, step=1)

st.sidebar.subheader("Custom Operations")
use_custom = st.sidebar.checkbox("Use Custom Operations", value=False)
if use_custom:
    op1 = st.sidebar.text_input("Operation for even numbers (use 'n')", "n // 2")
    op2 = st.sidebar.text_input("Operation for odd numbers (use 'n')", "3 * n + 1")
else:
    op1, op2 = None, None

# Button to Trigger Calculation
if st.button("Calculate Sequence"):
    # Generate the Sequence
    if max_steps == 0:
        sequence = generate_sequence(number, custom_ops=(op1, op2) if use_custom else None)
    else:
        sequence = generate_sequence(number, steps=max_steps, custom_ops=(op1, op2) if use_custom else None)

    # Display Results
    st.subheader("Generated Sequence")
    st.write(", ".join(map(str, sequence)))

    # Plotting
    st.subheader("Plots")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(sequence))), y=sequence, mode='lines+markers', name='Sequence'))
    fig.update_layout(title="Collatz Sequence", xaxis_title="Steps", yaxis_title="Value")
    st.plotly_chart(fig)

    # Logarithmic Plot
    st.subheader("Logarithmic Plot")
    log_sequence = [np.log10(y) if y > 0 else 0 for y in sequence]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=list(range(len(log_sequence))), y=log_sequence, mode='lines+markers', name='Log of Sequence', line=dict(color='orange')))
    fig.update_layout(title="Logarithmic Collatz Sequence", xaxis_title="Steps", yaxis_title="Log10(Value)")
    st.plotly_chart(fig)
