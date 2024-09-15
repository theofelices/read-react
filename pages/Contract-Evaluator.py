import streamlit as st
import pandas as pd
import numpy as np

# Function to normalize stats
def normalize_stat(stat, min_stat, max_stat):
    return (stat - min_stat) / (max_stat - min_stat) * 10

# Function to calculate composite score
def calculate_composite_score(ppg, rpg, apg, spg, bpg, fg, ft, to, three_fg, potential, draft_pos, role_adj, cap_adj):
    # Normalize the stats (using hypothetical min and max for demonstration)
    ppg_norm = normalize_stat(ppg, 0, 30)
    rpg_norm = normalize_stat(rpg, 0, 15)
    apg_norm = normalize_stat(apg, 0, 10)
    spg_norm = normalize_stat(spg, 0, 5)
    bpg_norm = normalize_stat(bpg, 0, 5)
    fg_norm = normalize_stat(fg, 0, 100)
    ft_norm = normalize_stat(ft, 0, 100)
    to_norm = normalize_stat(to, 0, 10)
    three_fg_norm = normalize_stat(three_fg, 0, 100)
    potential_norm = normalize_stat(potential, 0, 10)

    # Weighted composite score
    composite_score = (ppg_norm * 0.25) + (rpg_norm * 0.15) + (apg_norm * 0.15) + \
                      (spg_norm * 0.1) + (bpg_norm * 0.1) + (fg_norm * 0.05) + \
                      (ft_norm * 0.05) + (three_fg_norm * 0.1) + (potential_norm * 0.05) - (to_norm * 0.05)
    
    # Adjust composite score based on draft position, role, and cap
    draft_multiplier = 1 + (1 / draft_pos)  # Example: top 1 pick gets 2x, 2nd pick gets 1.5x, etc.
    composite_score *= draft_multiplier * role_adj * cap_adj

    return composite_score

# Function to determine salary based on composite score
def calculate_salary(composite_score):
    if composite_score >= 9:
        return "₱180,000 - ₱200,000 per month"
    elif composite_score >= 7:
        return "₱140,000 - ₱179,999 per month"
    elif composite_score >= 5:
        return "₱100,000 - ₱139,999 per month"
    elif composite_score >= 3:
        return "₱70,000 - ₱99,999 per month"
    else:
        return "₱50,000 - ₱69,999 per month"

# Function to determine if the player is a max contract candidate
def determine_max_contract(composite_score):
    if composite_score >= 9:
        return "Yes, this player is a max contract candidate."
    else:
        return "No, this player is not a max contract candidate."

# Streamlit app interface
st.title("Rookie Player Salary Calculator")
st.write("""
    Enter the player's statistics and other factors below to calculate the appropriate salary range for a rookie contract.
""")

# Input fields for player stats
ppg = st.number_input("Points per Game (PPG)", min_value=0.0, max_value=30.0, step=0.1)
rpg = st.number_input("Rebounds per Game (RPG)", min_value=0.0, max_value=15.0, step=0.1)
apg = st.number_input("Assists per Game (APG)", min_value=0.0, max_value=10.0, step=0.1)
spg = st.number_input("Steals per Game (SPG)", min_value=0.0, max_value=5.0, step=0.1)
bpg = st.number_input("Blocks per Game (BPG)", min_value=0.0, max_value=5.0, step=0.1)
fg = st.number_input("Field Goal Percentage (FG%)", min_value=0.0, max_value=100.0, step=0.1)
ft = st.number_input("Free Throw Percentage (FT%)", min_value=0.0, max_value=100.0, step=0.1)
to = st.number_input("Turnovers per Game (TO)", min_value=0.0, max_value=10.0, step=0.1)
three_fg = st.number_input("3-Point Field Goal Percentage (3P%)", min_value=0.0, max_value=100.0, step=0.1)
potential = st.slider("Potential and Development Score (1-10)", min_value=1, max_value=10, step=1)

# Additional input fields for draft position, role, and cap adjustment
draft_pos = st.number_input("Draft Position (1 for 1st pick, 2 for 2nd pick, etc.)", min_value=1, max_value=60, step=1)
role_adj = st.slider("Role Adjustment (1.0 for Bench, 1.5 for Rotation, 2.0 for Starter)", min_value=1.0, max_value=2.0, step=0.1)
cap_adj = st.slider("Cap Adjustment (0.5 for Tight Cap, 1.0 for Moderate, 1.5 for Cap Space)", min_value=0.5, max_value=1.5, step=0.1)

# Calculate composite score and salary
if st.button("Calculate Salary"):
    composite_score = calculate_composite_score(ppg, rpg, apg, spg, bpg, fg, ft, to, three_fg, potential, draft_pos, role_adj, cap_adj)
    salary_range = calculate_salary(composite_score)
    max_contract = determine_max_contract(composite_score)
    
    # Display results
    st.subheader(f"Composite Score: {composite_score:.2f}")
    st.subheader(f"Recommended Salary Range: {salary_range}")
    st.subheader(f"Max Contract Candidate: {max_contract}")
