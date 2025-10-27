import streamlit as st
import numpy as np
import plotly.graph_objects as go
from math import isfinite

# ---------- Core logic ----------
def collatz_step(n: int) -> int:
    """Perform a single step of the Collatz operation."""
    return n // 2 if n % 2 == 0 else 3 * n + 1

def _safe_eval(expr: str, n: int) -> int:
    """
    Evaluate a simple arithmetic expression referencing 'n' only.
    Restricts builtins and globals to reduce risk compared to raw eval.
    """
    return int(eval(expr, {"__builtins__": {}}, {"n": n}))

def custom_step(n: int, op1: str, op2: str) -> int:
    """Perform a custom operation based on user-defined expressions."""
    return _safe_eval(op1, n) if n % 2 == 0 else _safe_eval(op2, n)

def generate_sequence(n: int, steps: int | None = None, custom_ops: tuple[str, str] | None = None) -> list[int]:
    """Generate the sequence of numbers based on Collatz or custom operations."""
    if n <= 0:
        raise ValueError("Starting number must be a positive integer.")
    sequence = [n]
    seen = {n}
    max_iters = steps if (steps is not None and steps > 0) else 10**6  # Large default guard
    for _ in range(max_iters):
        if sequence[-1] == 1 and custom_ops is None:
            break
        next_num = custom_step(sequence[-1], *custom_ops) if custom_ops else collatz_step(sequence[-1])
        if next_num in seen:            # Detect repetition/cycle
            sequence.append(next_num)   # Include the repeated number for visibility
            break
        sequence.append(next_num)
        seen.add(next_num)
    return sequence

def seq_stats(seq: list[int]) -> dict:
    """Compute summary stats for a sequence."""
    odds = sum((x & 1) for x in seq)
    evens = len(seq) - odds
    ratio = (odds / evens) if evens else float("inf")
    return {
        "length": len(seq),
        "max_value": max(seq) if seq else None,
        "odds": odds,
        "evens": evens,
        "odd_even_ratio": ratio,
    }

# ---------- UI ----------
st.set_page_config(layout="wide")

# Initialize session state
st.session_state.setdefault("language", None)
st.session_state.setdefault("show_sequence1", False)
st.session_state.setdefault("show_sequence2", False)
st.session_state.setdefault("info_sequence1", False)
st.session_state.setdefault("info_sequence2", False)

# Language selection
if st.session_state.language is None:
    st.title("Choose Language / Scegli la Lingua")
    language = st.radio("Select your language / Seleziona la tua lingua:", ["English", "Italian"])
    if st.button("Start"):
        st.session_state.language = language
        st.stop()
else:
    lang = st.session_state.language

    # Text by language
    if lang == "English":
        title = "Collatz Conjecture Explorer"
        settings_title1 = "Settings for Sequence 1"
        settings_title2 = "Settings for Sequence 2"
        start_number = "Starting Number"
        max_steps = "Max Steps (0 for full sequence)"
        custom_operations = "Custom Operations"
        even_operation = "Operation for even numbers (uses 'n')"
        odd_operation = "Operation for odd numbers (uses 'n')"
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
        odds_label = "Odd count"
        evens_label = "Even count"
        ratio_label = "Odd/Even ratio"
        bad_input_msg = f"{start_number}: Invalid input (positive integer required)"
    else:
        title = "Esploratore della Congettura di Collatz"
        settings_title1 = "Impostazioni per Sequenza 1"
        settings_title2 = "Impostazioni per Sequenza 2"
        start_number = "Numero di partenza"
        max_steps = "Numero massimo di passi (0 per sequenza completa)"
        custom_operations = "Operazioni personalizzate"
        even_operation = "Operazione per numeri pari (usa 'n')"
        odd_operation = "Operazione per numeri dispari (usa 'n')"
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
        odds_label = "Numero di dispari"
        evens_label = "Numero di pari"
        ratio_label = "Rapporto dispari/pari"
        bad_input_msg = f"{start_number}: Valore non valido (richiesto intero positivo)"

    st.title(title)

    # --- Inputs for Sequence 1 ---
    st.sidebar.header(settings_title1, divider=True)
    number1_input = st.sidebar.text_input(start_number, "7", key="series1_number")
    max_steps1 = st.sidebar.number_input(max_steps, min_value=0, value=0, step=1, key="series1_steps")
    use_custom1 = st.sidebar.checkbox(custom_operations, value=False, key="series1_custom")
    if use_custom1:
        op1_1 = st.sidebar.text_input(even_operation, "n // 2", key="series1_op1")
        op2_1 = st.sidebar.text_input(odd_operation, "3 * n + 1", key="series1_op2")
    else:
        op1_1 = op2_1 = None

    # --- Inputs for Sequence 2 ---
    st.sidebar.header(settings_title2, divider=True)
    number2_input = st.sidebar.text_input(start_number, "10", key="series2_number")
    max_steps2 = st.sidebar.number_input(max_steps, min_value=0, value=0, step=1, key="series2_steps")
    use_custom2 = st.sidebar.checkbox(custom_operations, value=False, key="series2_custom")
    if use_custom2:
        op1_2 = st.sidebar.text_input(even_operation, "n // 2", key="series2_op1")
        op2_2 = st.sidebar.text_input(odd_operation, "3 * n + 1", key="series2_op2")
    else:
        op1_2 = op2_2 = None

    # Validate inputs
    def _parse_positive_int(txt: str) -> int | None:
        try:
            v = int(txt)
            return v if v > 0 else None
        except ValueError:
            return None

    number1 = _parse_positive_int(number1_input)
    if number1 is None:
        st.sidebar.error(bad_input_msg)

    number2 = _parse_positive_int(number2_input)
    if number2 is None:
        st.sidebar.error(bad_input_msg)

    # --- Sequence 1 ---
    if st.button(f"{calculate_sequence} 1") and number1 is not None:
        try:
            st.session_state['sequence1'] = generate_sequence(
                number1,
                steps=None if max_steps1 == 0 else max_steps1,
                custom_ops=(op1_1, op2_1) if use_custom1 else None
            )
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.get('sequence1'):
        sequence1 = st.session_state['sequence1']
        stats1 = seq_stats(sequence1)

        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(sequence1))), y=sequence1,
                                     mode='lines+markers', name='Sequence'))
            fig.update_layout(title=plot_title, xaxis_title=steps_label, yaxis_title=value_label)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            log_sequence1 = [np.log10(abs(float(y))) if y != 0 else 0 for y in sequence1]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(log_sequence1))), y=log_sequence1,
                                     mode='lines+markers', name='Log Sequence', line=dict(color='orange')))
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
                st.write(f"{sequence_length}: {stats1['length']}")
                st.write(f"{sequence_max_value}: {stats1['max_value']}")
                st.write(f"{odds_label}: {stats1['odds']}")
                st.write(f"{evens_label}: {stats1['evens']}")
                ratio_val = stats1['odd_even_ratio']
                ratio_text = f"{ratio_val:.6f}" if isfinite(ratio_val) else "∞"
                st.write(f"{ratio_label}: {ratio_text}")

    # --- Sequence 2 ---
    if st.button(f"{calculate_sequence} 2") and number2 is not None:
        try:
            st.session_state['sequence2'] = generate_sequence(
                number2,
                steps=None if max_steps2 == 0 else max_steps2,
                custom_ops=(op1_2, op2_2) if use_custom2 else None
            )
        except Exception as e:
            st.error(f"Error: {e}")

    if st.session_state.get('sequence2'):
        sequence2 = st.session_state['sequence2']
        stats2 = seq_stats(sequence2)

        col4, col5, col6 = st.columns([2, 2, 1])

        with col4:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(sequence2))), y=sequence2,
                                     mode='lines+markers', name='Sequence'))
            fig.update_layout(title=plot_title, xaxis_title=steps_label, yaxis_title=value_label)
            st.plotly_chart(fig, use_container_width=True)

        with col5:
            log_sequence2 = [np.log10(abs(float(y))) if y != 0 else 0 for y in sequence2]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=list(range(len(log_sequence2))), y=log_sequence2,
                                     mode='lines+markers', name='Log Sequence', line=dict(color='orange')))
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
                st.write(f"{sequence_length}: {stats2['length']}")
                st.write(f"{sequence_max_value}: {stats2['max_value']}")
                st.write(f"{odds_label}: {stats2['odds']}")
                st.write(f"{evens_label}: {stats2['evens']}")
                ratio_val = stats2['odd_even_ratio']
                ratio_text = f"{ratio_val:.6f}" if isfinite(ratio_val) else "∞"
                st.write(f"{ratio_label}: {ratio_text}")
