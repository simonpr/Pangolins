import streamlit as st

# 1. Initialize the Knowledge Base and State
if 'nodes' not in st.session_state:
    st.session_state.nodes = [
        None,
        ["DOES IT LIVE IN THE SEA", 4, 2],
        ["IS IT SCALY", 3, 5],
        ["DOES IT EAT ANTS", 6, 7],
        ["A WHALE", 0, 0],
        ["A BLANCMANGE", 0, 0],
        ["A PANGOLIN", 0, 0],
        ["AN ANT", 0, 0]
    ]
    st.session_state.current_idx = 1
    st.session_state.game_phase = "playing" # playing, guessing, learning, finished

st.title("📟 ZX Pangolins")
st.caption("Animal AI building (A modern web port of the 1982 Sinclair expert system).")

st.subheader(f"Think of an animal ?")

def restart_game():
    st.session_state.current_idx = 1
    st.session_state.game_phase = "playing"

# 2. Game Logic
if st.session_state.game_phase == "playing":
    node = st.session_state.nodes[st.session_state.current_idx]
    text, yes_idx, no_idx = node

    # Is it a question or an animal?
    if yes_idx == 0:
        st.session_state.game_phase = "guessing"
        st.rerun()
    else:
        st.subheader(f"{text}?")
        col1, col2 = st.columns(2)
        if col1.button("YES", use_container_width=True):
            st.session_state.current_idx = yes_idx
            st.rerun()
        if col2.button("NO", use_container_width=True):
            st.session_state.current_idx = no_idx
            st.rerun()

elif st.session_state.game_phase == "guessing":
    animal = st.session_state.nodes[st.session_state.current_idx][0]
    st.subheader(f"ARE YOU THINKING OF {animal}?")
    
    col1, col2 = st.columns(2)
    if col1.button("YES!", use_container_width=True):
        st.success("I THOUGHT AS MUCH.")
        st.session_state.game_phase = "finished"
        st.rerun()
    if col2.button("NO", use_container_width=True):
        st.session_state.game_phase = "learning"
        st.rerun()

elif st.session_state.game_phase == "learning":
    old_animal = st.session_state.nodes[st.session_state.current_idx][0]
    st.info(f"I don't know this animal. Help me learn!")
    
    with st.form("learning_form"):
        new_animal = st.text_input("WHAT IS IT THEN?").strip().upper()
        if new_animal and not new_animal.startswith("A "):
            new_animal = "A " + new_animal
            
        question = st.text_input(f"TELL ME A QUESTION WHICH DISTINGUISHES BETWEEN {old_animal} AND {new_animal}:").upper()
        ans_for_new = st.radio(f"WHAT IS THE ANSWER FOR {new_animal}?", ["YES", "NO"])
        
        if st.form_submit_button("TEACH ME"):
            if new_animal and question:
                # Update Tree logic
                new_idx = len(st.session_state.nodes)
                old_idx_copy = len(st.session_state.nodes) + 1
                
                # Add the two leaf nodes
                st.session_state.nodes.append([new_animal, 0, 0])
                st.session_state.nodes.append([old_animal, 0, 0])
                
                # Transform the old animal node into the new question node
                clean_q = question[:-1] if question.endswith('?') else question
                if ans_for_new == "YES":
                    st.session_state.nodes[st.session_state.current_idx] = [clean_q, new_idx, old_idx_copy]
                else:
                    st.session_state.nodes[st.session_state.current_idx] = [clean_q, old_idx_copy, new_idx]
                
                st.write("THAT FOOLED ME.")
                st.session_state.game_phase = "finished"
                st.rerun()

if st.session_state.game_phase == "finished":
    if st.button("PLAY AGAIN"):
        restart_game()
        st.rerun()

# 3. Debug: Show the "Brain" (Optional)
#with st.expander("View Knowledge Base"):
#    st.write(st.session_state.nodes)

