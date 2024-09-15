import streamlit as st

# Define the categories, their weights, and definitions
categories = {
    "On-Court Performance (25%)": {
        "weight": 0.25,
        "options": {
            1: "1-2: Poor performance, below league average, limited impact on games.",
            3: "3-4: Below average, occasional good performances but generally inconsistent.",
            5: "5-6: Average, reliable but not exceptional, good role player.",
            7: "7-8: Above average, consistently strong performance, potential All-Star.",
            9: "9-10: Elite, top performer, regularly impacts games significantly, MVP candidate."
        }
    },
    "Potential and Development (20%)": {
        "weight": 0.20,
        "options": {
            1: "1-2: Limited potential, likely at peak, minimal room for growth.",
            3: "3-4: Some potential but significant development unlikely.",
            5: "5-6: Moderate potential, could improve with good coaching and experience.",
            7: "7-8: High potential, showing steady improvement, likely future star.",
            9: "9-10: Exceptional potential, already improving rapidly, potential franchise player."
        }
    },
    "Contractual Situation (15%)": {
        "weight": 0.15,
        "options": {
            1: "1-2: Unfavorable contract, overpaid, long-term commitment with little flexibility.",
            3: "3-4: Below average, slightly overpaid, or unfavorable terms.",
            5: "5-6: Neutral, fairly compensated, average length and terms.",
            7: "7-8: Favorable contract, team-friendly, good value for performance.",
            9: "9-10: Extremely favorable, bargain deal, great flexibility for the team."
        }
    },
    "Marketability (10%)": {
        "weight": 0.10,
        "options": {
            1: "1-2: Little to no marketability, limited fan appeal.",
            3: "3-4: Below average marketability, some local appeal but limited broader impact.",
            5: "5-6: Average marketability, recognizable but not a major draw.",
            7: "7-8: High marketability, popular, attracts fans and media attention.",
            9: "9-10: Extremely marketable, superstar status, significant off-court revenue generation."
        }
    },
    "Injury History (10%)": {
        "weight": 0.10,
        "options": {
            1: "1-2: Very injury-prone, frequently misses games, long-term health concerns.",
            3: "3-4: Somewhat injury-prone, has missed significant time.",
            5: "5-6: Average durability, occasional injuries but generally reliable.",
            7: "7-8: Above average health, rarely injured, consistently available.",
            9: "9-10: Extremely durable, almost never injured, consistently plays full seasons."
        }
    },
    "Intangibles (10%)": {
        "weight": 0.10,
        "options": {
            1: "1-2: Poor leadership, negative impact on team chemistry, unprofessional.",
            3: "3-4: Below average intangibles, occasional issues with attitude or effort.",
            5: "5-6: Average intangibles, professional, neither significantly positive nor negative.",
            7: "7-8: Strong leadership, positive locker room presence, high work ethic.",
            9: "9-10: Exceptional intangibles, inspirational leader, greatly enhances team morale."
        }
    },
    "Team Needs (10%)": {
        "weight": 0.10,
        "options": {
            1: "1-2: Does not fit team needs at all, redundant or mismatched skills.",
            3: "3-4: Below average fit, some skills are useful but not a priority.",
            5: "5-6: Neutral fit, useful player but not a key addition.",
            7: "7-8: Good fit, addresses specific team needs and improves roster balance.",
            9: "9-10: Perfect fit, exactly what the team needs, significantly improves team dynamics."
        }
    }
}

# Function to calculate weighted score
def calculate_weighted_score(scores, categories):
    weighted_scores = {k: scores[k] * categories[k]["weight"] for k in scores}
    return sum(weighted_scores.values())

# App Title
st.title("Trade Machine")
st.write("Basketball trades can be complex, involving multiple teams, players, and draft picks. Understanding who got the best deal and evaluating the potential impact of each trade is crucial for fans, analysts, and team management alike. Our Trade Evaluator is designed to simplify this process by offering a detailed analysis of all trades.")

# Input number of eams
num_teams = st.number_input("Number of Teams Involved in Trade", min_value=2, max_value=4, value=2, step=1, key="num_teams")

# Input team names and traded players
team_info = {}
for i in range(1, num_teams + 1):
    team_name = st.text_input(f"Enter Team {i} Name", key=f"team_{i}_name")
    num_players_traded_to = st.number_input(f"Number of Players Traded To {team_name}", min_value=1, max_value=10, value=1, step=1, key=f"{i}_num_players_traded_to")
    players_traded_to = []
    for j in range(1, num_players_traded_to + 1):
        player_name = st.text_input(f"Name of Player Traded To {team_name}", key=f"{i}_player_traded_to_{j}")
        players_traded_to.append(player_name)
    team_info[team_name] = players_traded_to

# Form for scoring input
st.header("Input Scores")
with st.form("score_form"):
    scores = {}
    for team_name, players in team_info.items():
        st.subheader(f"Scores for {team_name}")
        for player in players:
            player_scores = {}
            for category, details in categories.items():
                player_scores[category] = st.selectbox(
                    f"Select score for {player} on {category}",
                    options=list(details["options"].keys()),
                    format_func=lambda x: details["options"][x],
                    key=f"{team_name}_{player}_{category}"
                )
            scores[player] = player_scores

    # Optional: Add draft picks
    draft_picks = {}
    st.header("Draft Picks")
    for team_name in team_info.keys():
        add_draft_pick = st.checkbox(f"Include a Draft Pick Acquired By {team_name}", key=f"{team_name}_draft_pick_checkbox")
        if add_draft_pick:
            draft_pick_position = st.selectbox(f"Draft Pick Acquired By {team_name}", ["Top 5", "Lottery", "Mid-First Round", "Late-First Round", "Second Round"], key=f"{team_name}_draft_pick_position")
            draft_pick_score = st.number_input(f"Estimate Draft Pick Value Acquired By {team_name}", min_value=1, max_value=10, key=f"{team_name}_draft_pick_score")
            draft_pick_weight = 0.10  # Standard weight for draft pick evaluation
            draft_picks[team_name] = draft_pick_score * draft_pick_weight

    submitted = st.form_submit_button("Calculate Trade Value")

# Display results after submission
if submitted:
    if all(team_info.values()):
        # Calculate and display weighted scores
        st.header("Trade Evaluation Results")
        team_scores = {}
        for team_name, players in team_info.items():
            team_weighted_score = sum([calculate_weighted_score(scores[player], categories) for player in players])
            if team_name in draft_picks:
                team_weighted_score += draft_picks[team_name]
            team_scores[team_name] = team_weighted_score
            st.write(f"**{team_name} Total Weighted Score:** :green[{team_weighted_score:.2f}]")

        # Combined Comparison Summary and Rankings
        st.header("Comparison Summary & Team Rankings")
        ranked_teams = sorted(team_scores.items(), key=lambda x: x[1], reverse=True)
        
        st.write("### Ranked Teams Based on Trade Evaluation:")
        for rank, (team_name, score) in enumerate(ranked_teams, start=1):
            st.write(f"{rank}. **{team_name}**: {score:.2f}")

        # Best and Worst Deal Identification
        best_team = ranked_teams[0][0]
        worst_team = ranked_teams[-1][0]
        
        if team_scores[best_team] == team_scores[worst_team]:
            st.info("The trade appears to be fair for all teams involved.")
        else:
            st.success(f"{best_team} is getting the best deal, while {worst_team} might be at a disadvantage based on the current evaluation.")

        # Contextual analysis on the draft picks
        st.header("Draft Pick Analysis")
        if draft_picks:
            for team_name, pick_score in draft_picks.items():
                st.write(f"**{team_name} Draft Pick Value:** {pick_score:.2f}")
                st.info(f"{team_name}'s draft pick value contributes significantly to their overall trade value.")
        else:
            st.info("No draft picks included.")
    else:
        st.error("Please enter all player names and team names to evaluate the trade.")
