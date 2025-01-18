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
    seen = set(sequence)
    for _ in range(steps if steps else 10**6):  # Large default max steps
        if sequence[-1] == 1:
            break
        if custom_ops:
            next_num = custom_step(sequence[-1], custom_ops[0], custom_ops[1])
        else:
            next_num = collatz_step(sequence[-1])
        if next_num in seen:  # Detect repetition
            sequence.append(next_num)  # Include the repeated number
            break
        sequence.append(next_num)
        seen.add(next_num)
    return sequence

### MAIN ###
st.set_page_config(layout="wide")

# Initialize session state variables
if "language" not in st.session_state:
    st.session_state.language = None
if "show_sequence1" not in st.session_state:
    st.session_state["show_sequence1"] = False
if "show_sequence2" not in st.session_state:
    st.session_state["show_sequence2"] = False
if "info_sequence1" not in st.session_state:
    st.session_state["info_sequence1"] = False
if "info_sequence2" not in st.session_state:
    st.session_state["info_sequence2"] = False

# Language selection
if "language" not in st.session_state:
    st.session_state.language = None

if st.session_state.language is None:
    st.title("Choose Language / Scegli la Lingua")
    language = st.radio("Select your language / Seleziona la tua lingua:", ["English", "Italian"])
    if st.button("Start"):
        st.session_state.language = language
        st.empty()
        st.stop()
else:
    lang = st.session_state.language

    # Define text for each language
    if lang == "English":
        title = "Collatz Conjecture Explorer"
        settings_title1 = "Settings for Sequence 1"
        settings_title2 = "Settings for Sequence 2"
        start_number = "Starting Number"
        max_steps = "Max Steps (0 for full sequence)"
        custom_operations = "Custom Operations"
        even_operation = "Operation for even numbers"
        odd_operation = "Operation for odd numbers"
        calculate_sequence = "Calculate Sequence"
        show_sequence = "Show Sequence"
        sequence_info = "Sequence Info"
        sequence_length = "Length of the sequence"
        sequence_max_value = "Maximum value in the sequence"
        plot_title = "Collatz Sequence"
        log_title = "Logarithm"
        steps_label = "Steps"
        value_label = "Value"
        log_value_label = "Log10(Value)"
    else:
        title = "Esploratore della Congettura di Collatz"
        settings_title1 = "Impostazioni per Sequenza 1"
        settings_title2 = "Impostazioni per Sequenza 2"
        start_number = "Numero di partenza"
        max_steps = "Numero massimo di passi (0 per sequenza completa)"
        custom_operations = "Operazioni personalizzate"
        even_operation = "Operazione per numeri pari"
        odd_operation = "Operazione per numeri dispari"
        calculate_sequence = "Calcola Sequenza"
        show_sequence = "Mostra Sequenza"
        sequence_info = "Informazioni"
        sequence_length = "Lunghezza della sequenza"
        sequence_max_value = "Valore massimo nella sequenza"
        plot_title = "Sequenza di Collatz"
        log_title = "Logaritmo"
        steps_label = "Passi"
        value_label = "Valore"
        log_value_label = "Log10(Valore)"

    st.title(title)

    # Inputs for both Series
    st.sidebar.header(settings_title1, divider=True)
    number1_input = st.sidebar.text_input(start_number, "7", key="series1_number")
    max_steps1 = st.sidebar.number_input(max_steps, min_value=0, value=0, step=1, key="series1_steps")

    use_custom1 = st.sidebar.checkbox(custom_operations, value=False, key="series1_custom")
    if use_custom1:
        op1_1 = st.sidebar.text_input(even_operation, "n // 2", key="series1_op1")
        op2_1 = st.sidebar.text_input(odd_operation, "3 * n + 1", key="series1_op2")
    else:
        op1_1, op2_1 = None, None

    # Repeat for Series 2
    st.sidebar.header(settings_title2, divider=True)
    number2_input = st.sidebar.text_input(start_number, "10", key="series2_number")
    max_steps2 = st.sidebar.number_input(max_steps, min_value=0, value=0, step=1, key="series2_steps")

    st.sidebar.subheader(custom_operations)
    use_custom2 = st.sidebar.checkbox(custom_operations, value=False, key="series2_custom")
    if use_custom2:
        op1_2 = st.sidebar.text_input(even_operation, "n // 2", key="series2_op1")
        op2_2 = st.sidebar.text_input(odd_operation, "3 * n + 1", key="series2_op2")
    else:
        op1_2, op2_2 = None, None

    # Validate inputs
    try:
        number1 = int(number1_input)
    except ValueError:
        st.sidebar.error(f"{start_number}: Invalid input")
        number1 = None

    try:
        number2 = int(number2_input)
    except ValueError:
        st.sidebar.error(f"{start_number}: Invalid input")
        number2 = None

    # Display outputs
    if st.button(f"{calculate_sequence} 1") and number1 is not None:
        if max_steps1 == 0:
            st.session_state['sequence1'] = generate_sequence(number1, custom_ops=(op1_1, op2_1) if use_custom1 else None)
        else:
            st.session_state['sequence1'] = generate_sequence(number1, steps=max_steps1, custom_ops=(op1_1, op2_1) if use_custom1 else None)
    if st.session_state.get('sequence1'):
        sequence1 = st.session_state['sequence1']

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(sequence1))), y=sequence1, mode='lines+markers', name='Sequence'))
            fig.update_layout(title=plot_title, xaxis_title=steps_label, yaxis_title=value_label)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            log_sequence1 = [np.log10(abs(float(y))) if y != 0 else 0 for y in sequence1]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(log_sequence1))), y=log_sequence1, mode='lines+markers', name='Log Sequence', line=dict(color='orange')))
            fig.update_layout(title=log_title, xaxis_title=steps_label, yaxis_title=log_value_label)
            st.plotly_chart(fig, use_container_width=True)

        with col3:
            if st.button(show_sequence, key="show_seq_1"):
                st.session_state['show_sequence1'] = not st.session_state['show_sequence1']

            if st.session_state['show_sequence1']:
                st.write(", ".join(map(str, sequence1)))

            if st.button(sequence_info, key="info_seq_1"):
                st.session_state['info_sequence1'] = not st.session_state['info_sequence1']

            if st.session_state['info_sequence1']:
                st.write(f"{sequence_length}: {len(sequence1)}")
                st.write(f"{sequence_max_value}: {max(sequence1)}")

    if st.button(f"{calculate_sequence} 2") and number2 is not None:
        if max_steps2 == 0:
            st.session_state['sequence2'] = generate_sequence(number2, custom_ops=(op1_2, op2_2) if use_custom2 else None)
        else:
            st.session_state['sequence2'] = generate_sequence(number2, steps=max_steps2, custom_ops=(op1_2, op2_2) if use_custom2 else None)
    if st.session_state.get('sequence2'):
        sequence2 = st.session_state['sequence2']

        col4, col5, col6 = st.columns([2, 2, 1])

        with col4:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(sequence2))), y=sequence2, mode='lines+markers', name='Sequence'))
            fig.update_layout(title=plot_title, xaxis_title=steps_label, yaxis_title=value_label)
            st.plotly_chart(fig, use_container_width=True)

        with col5:
            log_sequence2 = [np.log10(abs(float(y))) if y != 0 else 0 for y in sequence2]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(log_sequence2))), y=log_sequence2, mode='lines+markers', name='Log Sequence', line=dict(color='orange')))
            fig.update_layout(title=log_title, xaxis_title=steps_label, yaxis_title=log_value_label)
            st.plotly_chart(fig, use_container_width=True)

        with col6:
            if st.button(show_sequence, key="show_seq_2"):
                st.session_state['show_sequence2'] = not st.session_state['show_sequence2']

            if st.session_state['show_sequence2']:
                st.write(", ".join(map(str, sequence2)))

            if st.button(sequence_info, key="info_seq_2"):
                st.session_state['info_sequence2'] = not st.session_state['info_sequence2']

            if st.session_state['info_sequence2']:
                st.write(f"{sequence_length}: {len(sequence2)}")
                st.write(f"{sequence_max_value}: {max(sequence2)}")
