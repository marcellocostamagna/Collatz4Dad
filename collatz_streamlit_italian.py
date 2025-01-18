import streamlit as st
import numpy as np
import plotly.graph_objects as go

def collatz_step(n):
    """Esegue un singolo passo dell'operazione di Collatz."""
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

def custom_step(n, op1, op2):
    """Esegue un'operazione personalizzata basata su funzioni definite dall'utente."""
    if n % 2 == 0:
        return eval(op1)
    else:
        return eval(op2)

def generate_sequence(n, steps=None, custom_ops=None):
    """Genera la sequenza di numeri basata su Collatz o operazioni personalizzate."""
    sequence = [n]
    seen = set(sequence)
    for _ in range(steps if steps else 10**6):  
        if sequence[-1] == 1:
            break
        if custom_ops:
            next_num = custom_step(sequence[-1], custom_ops[0], custom_ops[1])
        else:
            next_num = collatz_step(sequence[-1])
        if next_num in seen: 
            sequence.append(next_num) 
            break
        sequence.append(next_num)
        seen.add(next_num)
    return sequence

### PRINCIPALE ###
st.set_page_config(layout="wide")
st.title("Esploratore della Congettura di Collatz")


# Inizializza lo stato della sessione per le sequenze
if 'sequence1' not in st.session_state:
    st.session_state['sequence1'] = None
if 'sequence2' not in st.session_state:
    st.session_state['sequence2'] = None
if 'show_sequence1' not in st.session_state:
    st.session_state['show_sequence1'] = False
if 'show_sequence2' not in st.session_state:
    st.session_state['show_sequence2'] = False
if 'info_sequence1' not in st.session_state:
    st.session_state['info_sequence1'] = False
if 'info_sequence2' not in st.session_state:
    st.session_state['info_sequence2'] = False

# Input utente per Serie 1
st.sidebar.header("Impostazioni per Sequenza 1", divider=True)
number1_input = st.sidebar.text_input("Numero di partenza ", "7", key="series1_number")
max_steps1 = st.sidebar.number_input("Numero massimo di passi (0 per sequenza completa) ", min_value=0, value=0, step=1, key="series1_steps")

use_custom1 = st.sidebar.checkbox("Usa operazioni personalizzate", value=False, key="series1_custom")
if use_custom1:
    op1_1 = st.sidebar.text_input("Operazione per numeri pari", "n // 2", key="series1_op1")
    op2_1 = st.sidebar.text_input("Operazione per numeri dispari", "3 * n + 1", key="series1_op2")
else:
    op1_1, op2_1 = None, None

# Input utente per Serie 2
st.sidebar.header("Impostazioni per Sequenza 2", divider=True)
number2_input = st.sidebar.text_input("Numero di partenza ", "10", key="series2_number")
max_steps2 = st.sidebar.number_input("Numero massimo di passi (0 per sequenza completa) ", min_value=0, value=0, step=1, key="series2_steps")

use_custom2 = st.sidebar.checkbox("Usa operazioni personalizzate", value=False, key="series2_custom")
if use_custom2:
    op1_2 = st.sidebar.text_input("Operazione per numeri pari", "n // 2", key="series2_op1")
    op2_2 = st.sidebar.text_input("Operazione per numeri dispari", "3 * n + 1", key="series2_op2")
else:
    op1_2, op2_2 = None, None

# Valida e converte gli input
try:
    number1 = int(number1_input)
except ValueError:
    st.sidebar.error("Input non valido per Numero di partenza (Sequenza 1). Inserisci un numero intero valido.")
    number1 = None

try:
    number2 = int(number2_input)
except ValueError:
    st.sidebar.error("Input non valido per Numero di partenza (Sequenza 2). Inserisci un numero intero valido.")
    number2 = None

# Bottone per calcolare la sequenza della Serie 1
if st.button("Calcola Sequenza 1") and number1 is not None:
    # Genera la sequenza per Serie 1
    if max_steps1 == 0:
        st.session_state['sequence1'] = generate_sequence(number1, custom_ops=(op1_1, op2_1) if use_custom1 else None)
    else:
        st.session_state['sequence1'] = generate_sequence(number1, steps=max_steps1, custom_ops=(op1_1, op2_1) if use_custom1 else None)
    st.session_state['show_sequence1'] = False
    st.session_state['info_sequence1'] = False

# Mostra e plotta i risultati per Serie 1
if st.session_state['sequence1']:
    sequence1 = st.session_state['sequence1']

    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(sequence1))), y=sequence1, mode='lines+markers', name='Sequenza'))
        fig.update_layout(title="Sequenza di Collatz", xaxis_title="Passi", yaxis_title="Valore")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        log_sequence1 = [np.log10(float(y)) if y > 0 else 0 for y in sequence1]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(log_sequence1))), y=log_sequence1, mode='lines+markers', name='Log della Sequenza', line=dict(color='orange')))
        fig.update_layout(title="Logaritmo", xaxis_title="Passi", yaxis_title="Log10(Valore)")
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        if st.button("Mostra Sequenza", key="show_seq_1"):
            st.session_state['show_sequence1'] = not st.session_state['show_sequence1']

        if st.session_state['show_sequence1']:
            st.write(", ".join(map(str, sequence1)))

        if st.button("Informazioni", key="info_seq_1"):
            st.session_state['info_sequence1'] = not st.session_state['info_sequence1']

        if st.session_state['info_sequence1']:
            st.write(f"Lunghezza della sequenza: {len(sequence1)}")
            st.write(f"Valore massimo nella sequenza: {max(sequence1)}")

# Bottone per calcolare la sequenza della Serie 2
if st.button("Calcola Sequenza 2") and number2 is not None:
    # Genera la sequenza per Serie 2
    if max_steps2 == 0:
        st.session_state['sequence2'] = generate_sequence(number2, custom_ops=(op1_2, op2_2) if use_custom2 else None)
    else:
        st.session_state['sequence2'] = generate_sequence(number2, steps=max_steps2, custom_ops=(op1_2, op2_2) if use_custom2 else None)
    st.session_state['show_sequence2'] = False
    st.session_state['info_sequence2'] = False

# Mostra e plotta i risultati per Serie 2
if st.session_state['sequence2']:
    sequence2 = st.session_state['sequence2']

    col4, col5, col6 = st.columns([2, 2, 1])

    with col4:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(sequence2))), y=sequence2, mode='lines+markers', name='Sequenza'))
        fig.update_layout(title="Sequenza di Collatz", xaxis_title="Passi", yaxis_title="Valore")
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        log_sequence2 = [np.log10(float(y)) if y > 0 else 0 for y in sequence2]
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=list(range(len(log_sequence2))), y=log_sequence2, mode='lines+markers', name='Log della Sequenza', line=dict(color='orange')))
        fig.update_layout(title="Logaritmo", xaxis_title="Passi", yaxis_title="Log10(Valore)")
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        if st.button("Mostra Sequenza", key="show_seq_2"):
            st.session_state['show_sequence2'] = not st.session_state['show_sequence2']

        if st.session_state['show_sequence2']:
            st.write(", ".join(map(str, sequence2)))
                     
        if st.button("Informazioni", key="info_seq_2"):
            st.session_state['info_sequence2'] = not st.session_state['info_sequence2']

        if st.session_state['info_sequence2']:
            st.write(f"Lunghezza della sequenza: {len(sequence2)}")
            st.write(f"Valore massimo nella sequenza: {max(sequence2)}")
