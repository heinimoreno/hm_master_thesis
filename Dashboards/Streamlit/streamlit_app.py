import streamlit as st
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.express as px

# Load data function
@st.cache_data
def load_csv(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return None

# File paths
players_file_path = r"C:/Users/moren/OneDrive/Desktop/HSLU/Master Thesis/Data/Scraping/FCZ/data/cleaned/players_complete.csv"
market_values_file_path = r"C:/Users/moren/OneDrive/Desktop/HSLU/Master Thesis/Data/Scraping/FCZ/data/cleaned/players_complete.csv"
similar_players_file_path = r"C:/Users/moren/OneDrive/Desktop/HSLU/Master Thesis/Data/Scraping/FCZ/data/cleaned/similar_players.csv"  
players_combined_file_path = r"C:/Users/moren/OneDrive/Desktop/HSLU/Master Thesis/Data/Scraping/FCZ/data/cleaned/players_complete.csv" 

# Load datasets
players_data = load_csv(players_file_path)
market_values_data = load_csv(market_values_file_path)
similar_players_data = load_csv(similar_players_file_path)
players_combined_data = load_csv(players_combined_file_path)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", [
    "Home",
    "In-depth Player Pathway Analysis",
    "Career Pathway & Competition Analysis"
])

# --- Home Page ---
if page == "Home":
    st.title("Welcome to the Player Pathways Analysis App")
    st.markdown(
        """
        Use the navigation menu on the left to explore different analyses:
        - **In-depth Player Pathway Analysis**: Explore similar players, minutes played, market value trends, and international games.
        - **Career Pathway & Competition Analysis**: Analyze career pathways and competition trends for players.
        - **A Nationalteam Player Analysis**: Analyze players who made it to the "A Nationalteam."
        """
    )

# --- In-depth Player Pathway Analysis ---
elif page == "In-depth Player Pathway Analysis":
    st.title("In-depth Player Pathway Analysis")

    # Filter Setup
    st.sidebar.subheader("Filter Options")
    selected_players = st.sidebar.multiselect(
        "Select Players for Analysis",
        options=sorted(players_data['Name'].unique()) if players_data is not None else [],
        default=[],
    )

    # Combine Player in Focus and Players to Compare
    #players_for_analysis = [player_in_focus] + players_to_compare if player_in_focus else players_to_compare

    # --- Similar Players Section ---
    st.header("Similar Players")
    if similar_players_data is not None and selected_players:
        player_to_analyze = selected_players[0]
        similar_data = similar_players_data[similar_players_data['Player Name'] == player_to_analyze]
        if not similar_data.empty:
            player_similar_data = similar_data.iloc[0]

            def get_arrow_color(score):
                if score >= 0.8:
                    return "green"
                elif 0.5 <= score < 0.8:
                    return "orange"
                else:
                    return "red"

            col1, col2, col3 = st.columns(3)

            # First similar player
            with col1:
                arrow_color = get_arrow_color(player_similar_data['Similarity Score 1'])
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <h5>First Similar Player</h5>
                        <h4>{player_similar_data['First Similar Player']}</h4>
                        <p style="color: {arrow_color}; font-weight: bold;">&#9650; Score: {player_similar_data['Similarity Score 1']:.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Second similar player
            with col2:
                arrow_color = get_arrow_color(player_similar_data['Similarity Score 2'])
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <h5>Second Similar Player</h5>
                        <h4>{player_similar_data['Second Similar Player']}</h4>
                        <p style="color: {arrow_color}; font-weight: bold;">&#9650; Score: {player_similar_data['Similarity Score 2']:.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            # Third similar player
            with col3:
                arrow_color = get_arrow_color(player_similar_data['Similarity Score 3'])
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <h5>Third Similar Player</h5>
                        <h4>{player_similar_data['Third Similar Player']}</h4>
                        <p style="color: {arrow_color}; font-weight: bold;">&#9650; Score: {player_similar_data['Similarity Score 3']:.2f}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.warning("No similar player data available for the selected Player in Focus.")
    else:
        st.warning("Similar Players data is not available or no Player in Focus selected.")

    # --- Minutes Played Analysis ---
    st.header("Minutes Played Analysis")
    if players_data is not None:
        filtered_data = players_data[players_data['Name'].isin(selected_players)]

        if not filtered_data.empty:
            filtered_data['Age in Season'] = filtered_data['Age in Season'].astype(int)
            # Generate a full range of ages and ensure no gaps
            min_age = filtered_data['Age in Season'].min()
            max_age = filtered_data['Age in Season'].max()
            all_ages = list(range(min_age, max_age + 1))

            # Create a DataFrame with all players and all ages
            expanded_data = pd.DataFrame(
                [(name, age) for name in selected_players for age in all_ages],
                columns=['Name', 'Age in Season']
            )

            # Merge with the original data to fill missing ages with zeros
            filtered_data = pd.merge(
                expanded_data,
                filtered_data,
                on=['Name', 'Age in Season'],
                how='left'
            ).fillna({'Played Minutes': 0, 'Competition': 'No Data'})

            # Add a combined Player-Age column for better X-axis labeling
            filtered_data['Player-Age'] = (
                filtered_data['Name'] + " (Age: " + filtered_data['Age in Season'].astype(str) + ")"
            )

            filtered_data = filtered_data.sort_values(['Age in Season', 'Name'], ascending=True)
            
            fig = px.bar(
                filtered_data,
                x='Player-Age',
                y='Played Minutes',
                color='Competition',
                title='Minutes Played by Player, Age, and Competition',
                labels={'Played Minutes': 'Minutes Played', 'Player-Age': 'Player (Age)'},
                barmode='stack',
            )
            # Ensure X-axis respects the correct order and does not group overlapping labels
            fig.update_layout(
                xaxis=dict(
                    tickangle=45,
                    categoryorder='array',
                    categoryarray=filtered_data['Player-Age'].unique()
                ),
                title_x=0.5,
                template='plotly_white',
                xaxis_tickfont=dict(size=8)
            )
            st.plotly_chart(fig, use_container_width=True)
            #fig.update_layout(xaxis_tickangle=45, title_x=0.5, template='plotly_white', xaxis=dict(categoryorder='array', categoryarray=filtered_data['Player-Age']))
            #st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No data available for the selected players.")
    else:
        st.error("Players data is not available.")

    # --- Market Value Development ---
    st.header("Market Value Development")
    if market_values_data is not None:
        filtered_market_data = market_values_data[market_values_data['Name'].isin(selected_players)] if selected_players else market_values_data

        if not filtered_market_data.empty:
            filtered_market_data = filtered_market_data.sort_values(['Player ID', 'Age in Season'])
            filtered_market_data['Relative_Change'] = (
                filtered_market_data.groupby('Player ID')['Market_Value']
                .pct_change()
                .fillna(0) * 100
            )

            # Absolute Market Value Chart
            fig_abs = px.line(
                filtered_market_data,
                x='Age in Season',
                y='Market_Value',
                color='Name',
                title="Absolute Market Values by Age",
                labels={'Market_Value': 'Market Value (€)', 'Age in Season': 'Age'},
            )
            fig_abs.update_layout(template='plotly_white', title_x=0.5)
            st.plotly_chart(fig_abs, use_container_width=True)

            # Relative Market Value Change Chart
            fig_rel = px.line(
                filtered_market_data,
                x='Age in Season',
                y='Relative_Change',
                color='Name',
                title="Relative Market Value Change by Age",
                labels={'Relative_Change': 'Relative Change (%)', 'Age in Season': 'Age'},
            )
            fig_rel.update_layout(template='plotly_white', title_x=0.5)
            st.plotly_chart(fig_rel, use_container_width=True)
        else:
            st.warning("No data available for the selected players.")
    else:
        st.error("Market values data is not available.")

    # --- International Games Analysis ---
    st.header("International Games Analysis")
    if players_data is not None:
        filtered_ig_data = players_data[
            (players_data['Competition'] == 'International') &
            (players_data['Name'].isin(selected_players))
        ] if selected_players else players_data[players_data['Competition'] == 'International']

        if not filtered_ig_data.empty:
            aggregated_data = filtered_ig_data.groupby(['Category', 'Name'])['Games Played'].sum().reset_index()

            fig_ig = px.bar(
                aggregated_data,
                x='Category',
                y='Games Played',
                color='Name',
                title="Games Played per National Team Level",
                labels={'Games Played': 'Sum of Games Played', 'Category': 'Team Level'},
                barmode='group',
            )
            fig_ig.update_layout(template='plotly_white', title_x=0.5)
            st.plotly_chart(fig_ig, use_container_width=True)
        else:
            st.warning("No data available for International games for the selected players.")
    else:
        st.error("Players data is not available.")

# --- Career Pathway & Competition Analysis ---
elif page == "Career Pathway & Competition Analysis":
    st.title("Career Pathway & Competition Analysis")

    # Selector for analysis type
    analysis_type = st.sidebar.radio(
        "Select Analysis Type",
        ["Career Pathway Overview", "Competition & Played Minutes Analysis"]
    )

    if analysis_type == "Career Pathway Overview":
        st.subheader("Career Pathway Overview")

        if players_data is not None:
            # Aggregate data by Category
            category_stats = players_data.groupby('Category')['Played Minutes'].agg(['sum', 'mean', 'count']).reset_index()
            category_stats.rename(columns={
                'sum': 'Total Played Minutes',
                'mean': 'Average Played Minutes',
                'count': 'Number of Entries'
            }, inplace=True)

            # Display the bar chart
            st.subheader("Played Minutes by Category")
            fig = px.bar(
                category_stats,
                x='Category',
                y='Total Played Minutes',
                title="Total Played Minutes by Category",
                labels={'Total Played Minutes': 'Total Minutes', 'Category': 'Competition Category'},
                text='Total Played Minutes'
            )
            fig.update_layout(template="plotly_white", title_x=0.5)
            st.plotly_chart(fig, use_container_width=True)

            # Show raw data
            st.subheader("Raw Category Stats")
            st.dataframe(category_stats)
        else:
            st.error("Players data is not available.")
    


    elif analysis_type == "Competition & Played Minutes Analysis":
        st.subheader("Competition & Played Minutes Analysis (Non-'International' Competitions, Players Younger Than 21)")

        if players_data is not None:
            # Step 1: Extract Player IDs for "A Nationalteam"
            a_nationalteam_ids = players_data[players_data['Category'] == 'A Nationalteam']['Player ID'].unique()

            if len(a_nationalteam_ids) > 0:
                # Step 2: Filter for these Player IDs, excluding "International" and keeping multiple rows per ID
                relevant_data = players_data[
                    (players_data['Player ID'].isin(a_nationalteam_ids)) &
                    (players_data['Competition'] != 'International') &
                    (players_data['Type'] == 'Nationale Ligen') &
                    (players_data['Age in Season'] < 21)
                ]
                # Step 3: Remove Outliers (competitions with fewer than 3 players or low total played minutes)
                competition_player_counts = relevant_data.groupby('Competition')['Player ID'].nunique()
                competition_played_minutes = relevant_data.groupby('Competition')['Played Minutes'].sum()

                # Keep competitions with at least 3 unique players and total played minutes >= 1000
                valid_competitions = competition_player_counts[
                    (competition_player_counts >= 5) &
                    (competition_played_minutes >= 1000)
                ].index

                relevant_data = relevant_data[relevant_data['Competition'].isin(valid_competitions)]

                if not relevant_data.empty:
                    # Network Graph Construction
                    st.subheader("Network Graph: Competition Connections")

                    # Prepare graph data
                    G = nx.Graph()

                    # Add nodes with sizes proportional to the number of players in each competition
                    node_sizes = relevant_data.groupby('Competition')['Player ID'].nunique().to_dict()
                    for competition, size in node_sizes.items():
                        G.add_node(competition, size=size)

                    # Add edges based on shared players between competitions
                    for player_id, group in relevant_data.groupby('Player ID'):
                        competitions = group['Competition'].unique()
                        for i, competition1 in enumerate(competitions):
                            for competition2 in competitions[i + 1:]:
                                if G.has_edge(competition1, competition2):
                                    G[competition1][competition2]['weight'] += 1
                                else:
                                    G.add_edge(competition1, competition2, weight=1)

                    # Visualize the network graph
                    pos = nx.spring_layout(G, seed=42)  # Spring layout for node positioning
                    node_sizes_scaled = [G.nodes[node]['size'] * 50 for node in G.nodes]  # Scale node sizes
                    edge_weights = nx.get_edge_attributes(G, 'weight')  # Edge weights

                    plt.figure(figsize=(12, 8))
                    nx.draw_networkx_nodes(G, pos, node_size=node_sizes_scaled, node_color='skyblue')
                    nx.draw_networkx_edges(G, pos, width=[weight * 0.2 for weight in edge_weights.values()], edge_color='gray')
                    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black', font_weight='bold')
                    nx.draw_networkx_edge_labels(
                        G,
                        pos,
                        edge_labels={k: f"{v}" for k, v in edge_weights.items()},
                        font_size=8
                    )

                    st.pyplot(plt)

                    # Generate Table of Top 5 Leagues Based on Connections and Weights
                    st.subheader("Top 5 Leagues Based on Connections and Weights")

                    # Get the degree of each node (sum of weights of connections for each node)
                    degree_dict = dict(G.degree(weight='weight'))

                    # Convert degree information into a Pandas DataFrame
                    league_stats = pd.DataFrame({
                        'League': degree_dict.keys(),
                        'Total Connections (Weights)': degree_dict.values(),
                        'Players (Node Size)': [G.nodes[league]['size'] for league in degree_dict.keys()]
                    })

                    # Sort by total connection weights in descending order
                    league_stats = league_stats.sort_values(by='Total Connections (Weights)', ascending=False)

                    # Display the top 5 leagues
                    st.table(league_stats.head(5))

                    # Display raw data for reference
                    st.subheader("Filtered Data (Non-'International' Competitions, Under 21)")
                    st.dataframe(relevant_data)
                else:
                    st.warning("No data available for the selected filters (non-'International', under 21).")
            else:
                st.warning("No players found who reached the 'A Nationalteam'.")
        else:
            st.error("Players data is not available.")

    
