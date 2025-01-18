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
    for _ in range(steps if steps else 10**6):  # Large default max steps
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

# Initialize session state for sequences
if 'sequence1' not in st.session_state:
    st.session_state['sequence1'] = None
if 'sequence2' not in st.session_state:
    st.session_state['sequence2'] = None

# User Inputs for Series 1
st.sidebar.header("Settings for Series 1")
number1 = st.sidebar.number_input("Starting Number (Series 1)", min_value=-1000, value=7, step=1, key="series1_number")
max_steps1 = st.sidebar.number_input("Max Steps (0 for full sequence to 1) (Series 1)", min_value=0, value=0, step=1, key="series1_steps")

st.sidebar.subheader("Custom Operations for Series 1")
use_custom1 = st.sidebar.checkbox("Use Custom Operations (Series 1)", value=False, key="series1_custom")
if use_custom1:
    op1_1 = st.sidebar.text_input("Operation for even numbers (use 'n') (Series 1)", "n // 2", key="series1_op1")
    op2_1 = st.sidebar.text_input("Operation for odd numbers (use 'n') (Series 1)", "3 * n + 1", key="series1_op2")
else:
    op1_1, op2_1 = None, None

# User Inputs for Series 2
st.sidebar.header("Settings for Series 2")
number2 = st.sidebar.number_input("Starting Number (Series 2)", min_value=-1000, value=10, step=1, key="series2_number")
max_steps2 = st.sidebar.number_input("Max Steps (0 for full sequence to 1) (Series 2)", min_value=0, value=0, step=1, key="series2_steps")

st.sidebar.subheader("Custom Operations for Series 2")
use_custom2 = st.sidebar.checkbox("Use Custom Operations (Series 2)", value=False, key="series2_custom")
if use_custom2:
    op1_2 = st.sidebar.text_input("Operation for even numbers (use 'n') (Series 2)", "n // 2", key="series2_op1")
    op2_2 = st.sidebar.text_input("Operation for odd numbers (use 'n') (Series 2)", "3 * n + 1", key="series2_op2")
else:
    op1_2, op2_2 = None, None

# Button to Trigger Calculation for Series 1
if st.button("Calculate Sequence for Series 1"):
    # Generate the Sequence for Series 1
    if max_steps1 == 0:
        st.session_state['sequence1'] = generate_sequence(number1, custom_ops=(op1_1, op2_1) if use_custom1 else None)
    else:
        st.session_state['sequence1'] = generate_sequence(number1, steps=max_steps1, custom_ops=(op1_1, op2_1) if use_custom1 else None)

# Button to Trigger Calculation for Series 2
if st.button("Calculate Sequence for Series 2"):
    # Generate the Sequence for Series 2
    if max_steps2 == 0:
        st.session_state['sequence2'] = generate_sequence(number2, custom_ops=(op1_2, op2_2) if use_custom2 else None)
    else:
        st.session_state['sequence2'] = generate_sequence(number2, steps=max_steps2, custom_ops=(op1_2, op2_2) if use_custom2 else None)

# Display and Plot Results for Series 1
if st.session_state['sequence1']:
    sequence1 = st.session_state['sequence1']
    st.subheader("Generated Sequence for Series 1")
    st.write(", ".join(map(str, sequence1)))

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Plot (Series 1)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(sequence1))), y=sequence1, mode='lines+markers', name='Sequence 1'))
        fig.update_layout(title="Collatz Sequence (Series 1)", xaxis_title="Steps", yaxis_title="Value")
        st.plotly_chart(fig)

    with col2:
        st.subheader("Logarithmic Plot (Series 1)")
        log_sequence1 = [np.log10(y) if y > 0 else 0 for y in sequence1]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(log_sequence1))), y=log_sequence1, mode='lines+markers', name='Log of Sequence 1', line=dict(color='orange')))
        fig.update_layout(title="Logarithmic Collatz Sequence (Series 1)", xaxis_title="Steps", yaxis_title="Log10(Value)")
        st.plotly_chart(fig)

# Display and Plot Results for Series 2
if st.session_state['sequence2']:
    sequence2 = st.session_state['sequence2']
    st.subheader("Generated Sequence for Series 2")
    st.write(", ".join(map(str, sequence2)))

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Plot (Series 2)")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(sequence2))), y=sequence2, mode='lines+markers', name='Sequence 2'))
        fig.update_layout(title="Collatz Sequence (Series 2)", xaxis_title="Steps", yaxis_title="Value")
        st.plotly_chart(fig)

    with col4:
        st.subheader("Logarithmic Plot (Series 2)")
        log_sequence2 = [np.log10(y) if y > 0 else 0 for y in sequence2]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(log_sequence2))), y=log_sequence2, mode='lines+markers', name='Log of Sequence 2', line=dict(color='orange')))
        fig.update_layout(title="Logarithmic Collatz Sequence (Series 2)", xaxis_title="Steps", yaxis_title="Log10(Value)")
        st.plotly_chart(fig)
