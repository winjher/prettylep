# import streamlit as st
# import os
# import plotly.express as px
# import pandas as pd
# import datetime
# # from modules.breeding_management import breeding_management_app # Assuming this is available

# # Helper Functions (Metrics)
# # ---

# def get_active_batches_count():
#     """Get count of active breeding batches"""
#     try:
#         if os.path.exists('breeding_batches.csv'):
#             df = pd.read_csv('breeding_batches.csv')
#             return len(df)
#     except:
#         pass
#     return 0

# def get_species_count():
#     """Get count of butterfly species (Placeholder logic)"""
#     # Assuming the module or data structure exists, using a placeholder return
#     # from Data.butterfly_species_info import BUTTERFLY_SPECIES_INFO
#     # return len(BUTTERFLY_SPECIES_INFO)
#     return 15

# def get_monthly_sales():
#     """Get monthly sales count"""
#     try:
#         from datetime import datetime, timedelta
#         if os.path.exists('butterfly_purchases.csv'):
#             df = pd.read_csv('butterfly_purchases.csv')
#             # Filter for current month
#             current_month = datetime.now().replace(day=1)
#             df['Date'] = pd.to_datetime(df['Date'])
#             monthly_sales = df[df['Date'] >= current_month]
#             return len(monthly_sales)
#     except:
#         pass
#     return 0

# def get_booking_count():
#     """Get farm booking count"""
#     try:
#         if os.path.exists('farm_bookings.csv'):
#             df = pd.read_csv('farm_bookings.csv')
#             return len(df)
#     except:
#         pass
#     return 0

# def get_premium_users_count():
#     """Get count of premium users"""
#     try:
#         if os.path.exists('users.csv'):
#             df = pd.read_csv('users.csv')
#             premium_users = df[df['is_premium'] == True]
#             return len(premium_users)
#     except:
#         pass
#     return 0

# # Core Visualization Function
# # ---

# def classification_trends_content(classifications_df):
#     """Visualize AI classification trends over time in a dedicated container"""
    
#     st.subheader("AI Classification Trends Over Time")
    
#     # --- Data Processing for Trends ---
#     # Ensure timestamp is datetime and handle potential errors
#     if 'timestamp' in classifications_df.columns:
#         classifications_df['timestamp'] = pd.to_datetime(classifications_df['timestamp'], errors='coerce')
#         # Drop rows where datetime conversion failed
#         classifications_df = classifications_df.dropna(subset=['timestamp'])
#     else:
#         st.error("Missing 'timestamp' column for trend analysis.")
#         return

#     # Filter out empty predicted species for the scatter plot
#     species_df = classifications_df[classifications_df['predicted_species'].notna() & (classifications_df['predicted_species'] != "")]

#     # --- Sidebar Filters ---
#     st.sidebar.header("Filters")
    
#     # Filter for User
#     if 'user' in classifications_df.columns:
#         user_filter = st.sidebar.multiselect(
#             "Select User(s)",
#             classifications_df['user'].unique(),
#             default=classifications_df['user'].unique()
#         )
#         filtered_df = species_df[species_df['user'].isin(user_filter)]
#     else:
#         st.sidebar.warning("No 'user' column found.")
#         filtered_df = species_df
        
#     # Filter for Analysis Type
#     if 'analysis_type' in classifications_df.columns:
#         analysis_filter = st.sidebar.multiselect(
#             "Select Analysis Type(s)",
#             classifications_df['analysis_type'].unique(),
#             default=classifications_df['analysis_type'].unique()
#         )
#         filtered_df = filtered_df[filtered_df['analysis_type'].isin(analysis_filter)]
    
#     # --- Chart: Species Over Time (Scatter Plot) ---
#     st.markdown("### Species Predictions Over Time")
#     if not filtered_df.empty:
#         fig = px.scatter(
#             filtered_df,
#             x='timestamp',
#             y='predicted_species',
#             size='species_confidence',
#             color='user',
#             hover_data=['analysis_type', 'species_confidence'],
#             title="Species Predictions Over Time (Filtered)",
#             height=600
#         )
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.warning("No species data available for selected filters.")

#     # --- Optional: Show confidence trend for each species (Line Plot) ---
#     st.markdown("---")
#     if st.checkbox("Show species confidence trend over time"):
#         st.markdown("### Species Confidence Trend")
#         if not filtered_df.empty:
#             # Group data for line plot (e.g., average confidence per week for each species)
#             conf_df = filtered_df.copy()
#             conf_df['week'] = conf_df['timestamp'].dt.to_period('W').astype(str)
            
#             weekly_confidence = conf_df.groupby(['week', 'predicted_species'])['species_confidence'].mean().reset_index()
#             weekly_confidence.rename(columns={'species_confidence': 'Average Confidence'}, inplace=True)
            
#             fig2 = px.line(
#                 weekly_confidence,
#                 x='week',
#                 y='Average Confidence',
#                 color='predicted_species',
#                 title="Average Species Confidence Trend by Week",
#                 markers=True
#             )
#             st.plotly_chart(fig2, use_container_width=True)
#         else:
#              st.warning("No data available to plot confidence trend.")


# def dashboard_app():
#     """Dashboard overview of the entire ecosystem"""
#     st.title("🦋 LepVision Dashboard")
#     st.markdown("Welcome to the LepVision Dashboard! Here you can get an overview of your butterfly breeding ecosystem.")

#     # --- 1. Key Metrics Container ---
#     st.container(border=True)
#     st.header("Key Operational Metrics")
#     col1, col2, col3, col4 = st.columns(4)
#     with col1:
#         active_batches = get_active_batches_count()
#         st.metric("**Active Breeding Batches**", active_batches)
#     with col2:
#         species_count = get_species_count()
#         st.metric("**Butterfly Species**", species_count)
#     with col3:
#         monthly_sales = get_monthly_sales()
#         st.metric("**Monthly Sales**", monthly_sales)
#     with col4:
#         booking_count = get_booking_count()
#         st.metric("**Farm Bookings**", booking_count)

#     # --- Data Loading (Centralized) ---
#     try:
#         # Load the CSV. Using relative path should work if the file is present.
#         classifications_df = pd.read_csv("ai_classifications.csv")
#         # Clean up missing columns
#         classifications_df = classifications_df.fillna("")
#     except FileNotFoundError:
#         st.error("`ai_classifications.csv` not found. Cannot display classification stats.")
#         # Create an empty dataframe to prevent errors in subsequent code
#         classifications_df = pd.DataFrame(columns=['timestamp', 'predicted_species', 'predicted_stage', 'predicted_disease', 'predicted_defect'])
#     except Exception as e:
#         st.error(f"Error loading `ai_classifications.csv`: {e}")
#         classifications_df = pd.DataFrame(columns=['timestamp', 'predicted_species', 'predicted_stage', 'predicted_disease', 'predicted_defect'])
        
#     # --- 2. Classification Statistics Container ---
#     with st.container(border=True):
#         st.header("AI Classification Statistics")
#         col1, col2, col3, col4, col5, col6 = st.columns(6)
        
#         with col1:
#             st.metric("**Total Classifications**", len(classifications_df))
#         with col2:
#             # Count non-empty species classifications
#             species_count = classifications_df['predicted_species'].notna().sum()
#             st.metric("**Species Identified**", species_count)
#         with col3:
#             # Count non-empty life stage classifications
#             stage_count = classifications_df['predicted_stage'].notna().sum()
#             st.metric("**Life Stages Classified**", stage_count)
#         with col4:
#             # Count non-empty larval disease classifications
#             disease_count = classifications_df['predicted_disease'].notna().sum()
#             st.metric("**Larval Diseases Classified**", disease_count)
#         with col5:
#             # Count non-empty pupae defect classifications
#             defect_count = classifications_df['predicted_defect'].notna().sum()
#             st.metric("**Pupae Defects Classified**", defect_count)
#         with col6:
#             if 'timestamp' in classifications_df.columns:
#                 today = datetime.date.today().strftime('%Y-%m-%d')
#                 # Ensure timestamp is string for comparison
#                 today_classifications = len(classifications_df[classifications_df['timestamp'].astype(str).str.startswith(today)])
#                 st.metric("**Today's Classifications**", today_classifications)
#             else:
#                  st.metric("**Today's Classifications**", "N/A")


#     st.markdown("---")

#     # --- 3. Classification Trends Container ---
#     with st.container(border=True):
#         st.header("📈 AI Classification Trends")
#         classification_trends_content(classifications_df)


# # This is the entry point for the Streamlit app
# if __name__ == "__main__":
#     # Assuming this script is run directly by Streamlit
#     dashboard_app()

import streamlit as st
import os
import plotly.express as px
import pandas as pd
import datetime
from io import StringIO
# from modules.breeding_management import breeding_management_app # Assuming this is available
AI_classifications =pd.read_csv("ai_classifications.csv")
# --- Helper Functions (Metrics) ---
# NOTE: These functions are stubs since the data files don't exist in the environment
def get_active_batches_count():
    """Get count of active breeding batches"""
    # Using a dummy value since file reading is commented out
    # try:
    #     if os.path.exists('breeding_batches.csv'):
    #         df = pd.read_csv('breeding_batches.csv')
    #         return len(df)
    # except:
    #     pass
    return 12

def get_species_count():
    """Get count of butterfly species (Placeholder logic)"""
    return 18

def get_monthly_sales():
    """Get monthly sales count"""
    return 350 # Dummy Value

def get_booking_count():
    """Get farm booking count"""
    return 42 # Dummy Value

# --- Core Visualization Function ---

def classification_trends_content(classifications_df):
    """
    Visualize AI classification trends over time.
    This function handles the logic for filters and charts.
    """
    
    # --- Data Processing for Trends ---
    if 'timestamp' in classifications_df.columns:
        classifications_df['timestamp'] = pd.to_datetime(classifications_df['timestamp'], errors='coerce')
        classifications_df = classifications_df.dropna(subset=['timestamp'])
    else:
        st.error("Missing 'timestamp' column for trend analysis.")
        return

    species_df = classifications_df[classifications_df['predicted_species'].notna() & (classifications_df['predicted_species'] != "")]

    # --- Sidebar Filters ---
    st.sidebar.header("🔍 Filter AI Data")
    filtered_df = species_df.copy()
    
    with st.sidebar.expander("Apply Filters", expanded=True):
        
        # Filter for User
        if 'user' in filtered_df.columns:
            user_filter = st.multiselect(
                "Select User(s)",
                filtered_df['user'].unique(),
                default=filtered_df['user'].unique()
            )
            filtered_df = filtered_df[filtered_df['user'].isin(user_filter)]
        
        # Filter for Analysis Type
        if 'analysis_type' in filtered_df.columns:
            analysis_filter = st.multiselect(
                "Select Analysis Type(s)",
                filtered_df['analysis_type'].unique(),
                default=filtered_df['analysis_type'].unique()
            )
            filtered_df = filtered_df[filtered_df['analysis_type'].isin(analysis_filter)]

    # --- Chart 1: Species Over Time (Scatter Plot) ---
    st.subheader("Species Predictions Over Time")
    
    if not filtered_df.empty:
        fig = px.scatter(
            filtered_df,
            x='timestamp',
            y='predicted_species',
            size='species_confidence',
            color='user',
            hover_data=['analysis_type', 'species_confidence'],
            title="Species Classification Trend by User",
            height=500
        )
        fig.update_layout(template="seaborn", margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No species data available for selected filters.")

    # --- Chart 2: Optional Confidence Trend (Line Plot) ---
    st.markdown("---")
    if st.checkbox("Show Average Species Confidence Trend"):
        
        conf_df = filtered_df.copy()
        if not conf_df.empty:
            conf_df['week'] = conf_df['timestamp'].dt.to_period('W').astype(str)
            
            weekly_confidence = conf_df.groupby(['week', 'predicted_species'])['species_confidence'].mean().reset_index()
            weekly_confidence.rename(columns={'species_confidence': 'Average Confidence'}, inplace=True)
            
            fig2 = px.line(
                weekly_confidence,
                x='week',
                y='Average Confidence',
                color='predicted_species',
                title="Weekly Average Species Confidence",
                markers=True,
                height=400
            )
            fig2.update_layout(template="seaborn", margin=dict(t=50, b=0, l=0, r=0))
            st.plotly_chart(fig2, use_container_width=True)
        else:
             st.info("Filter selection is too narrow to plot confidence trend.")


def dashboard_app():
    """Dashboard overview of the entire ecosystem"""
    st.set_page_config(layout="wide")
    st.title("🦋 LepVision Dashboard:Overview")
    st.markdown("Welcome! This dashboard provides **key operational metrics** and **AI classification trends** for breeding program.")
    
    # --- Data Loading (Centralized) ---
    try:
        
        csv_data = """timestamp,analysis_type,user,predicted_species,species_confidence,predicted_stage,stage_confidence,predicted_disease,disease_confidence,predicted_defect,defect_confidence
2025-07-28 03:05:56,Species Identification,jerwin,Butterfly-Clippers,0.9563799119614895,,,,,
2025-07-28 03:50:05,Lifecycle Stage,jerwin,,,,,0.9289526844470476,,,
2025-07-28 04:14:20,Complete Analysis (All Models),eric,Butterfly-Tailed Jay,0.8894933792916009,Eggs,0.9414944652127123,Nucleopolyhedrosis,0.7079365537575126,Deformed body,0.8832724480031751
2025-08-02 09:11:21,Complete Analysis (All Models),admin,Butterfly-Emerald Swallowtail,0.8795377702805264,Pupae,0.8201825153922885,Gnathostomiasis,0.7970243525776469,Overbend,0.8556075770748914
2025-09-05 12:47:24,Complete Analysis (All Models),Guest User,Butterfly-Golden Birdwing,0.9998904466629028,Butterfly,1.0,Healthy,0.780186116695404,Healthy Pupae,0.9999998807907104
2025-09-05 13:17:41,Larval Disease Detection,Guest User,,,Healthy,0.9371570348739624,,,
2025-10-08 14:44:23,Lifecycle Stage,Guest User,,,Butterfly,0.9999719858169556,,,
2025-10-14 15:52:14,Species Identification,sarah,Butterfly-Common Jay,0.9939047694206238,,,,,
2025-10-15 15:31:52,Lifecycle Stage,hei,,,Butterfly,0.9999990463256836,,,
2025-10-16 15:15:16,Species Identification,jerwin,Butterfly-Golden Birdwing,0.9994238615036011,,,,,
2025-10-19 14:13:03,Larval Disease Detection,jerwin,,,Nucleopolyhedrosis,0.9975722432136536,,,
2025-11-03 18:24:07,Pupae Defect Analysis,dennis,,,,,,,,Deformed body,0.8586932420730591
2025-11-07 15:29:43,Lifecycle Stage,jerwin,,,Butterfly,1.0,,,
"""
        
        classifications_df = pd.read_csv(StringIO(csv_data), on_bad_lines='skip')
        classifications_df = classifications_df.fillna("")
    except Exception as e:
        st.error(f"Error loading classification data: {e}")
        classifications_df = pd.DataFrame(columns=['timestamp', 'predicted_species', 'predicted_stage', 'predicted_disease', 'predicted_defect', 'user', 'species_confidence'])
        
    
    # --- 1. Key Metrics Container (Top Row) - CARDS IMPLEMENTED ---
    with st.container(border=False):
        st.subheader("Operational Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            with st.container(border=True): # Card 1
                active_batches = get_active_batches_count()
                st.markdown(f"**📦 Active Batches**")
                st.metric("", active_batches, delta="New")
                
        with col2:
            with st.container(border=True): # Card 2
                species_count = get_species_count()
                st.markdown(f"**🦋 Species in Farm**")
                st.metric("", species_count, delta="▲ 2%")
                
        # with col3:
        #     with st.container(border=True): # Card 3
        #         monthly_sales = get_monthly_sales()
        #         st.markdown(f"**💰 Monthly Sales**")
        #         st.metric("", f"${monthly_sales:,}", delta="▲ 10%")
                
        # with col4:
        #     with st.container(border=True): # Card 4
        #         booking_count = get_booking_count()
        #         st.markdown(f"**🗓️ Farm Bookings**")
        #         st.metric("", booking_count, delta="New")

    st.markdown("---")

    # --- 2. Classification Statistics Container (Second Row) - CARDS IMPLEMENTED ---
    with st.container(border=True):
     #import pandas as pd
        classifications_df = pd.read_csv("ai_classifications.csv")
        st.write("**Classification Statistics:**")
        col1, col2, col3, col4, col5, col6 = st.columns(6)
                
        with col1:
            st.metric("Total Classifications", len(classifications_df))
        with col2:
            # Count non-empty species classifications
            species_count = (classifications_df['analysis_type']
            .isin(["Complete Analysis (All Models)", "Species Identification"])).sum()
            st.metric("Species Identified", species_count)
        with col3:
            # Count non-empty life stage classifications
            stage_count = (classifications_df['analysis_type']
            .isin(["Complete Analysis (All Models)", "Lifecycle Stage"])).sum()
            st.metric("Life Stages Classified", stage_count)
        with col4:
            # Count non-empty larval disease classifications
            disease_count = (classifications_df['analysis_type']
            .isin(["Complete Analysis (All Models)", "Larval Disease Detection"])).sum()
            st.metric("Larval Diseases Classified", disease_count)
        with col5:
            # Count non-empty pupae defect classifications
            defect_count = (classifications_df['analysis_type']
            .isin(["Complete Analysis (All Models)", "Pupae Defect Analysis"])).sum()
            st.metric("Pupae Defects Classified", defect_count)
        with col6:
            today = datetime.date.today().strftime('%Y-%m-%d')
            today_classifications = len(classifications_df[classifications_df['timestamp'].astype(str).str.startswith(today)])
            st.metric("Today's Classifications", today_classifications)

    # --- 3. Classification Trends Container (Main Chart Section) ---
    with st.container(border=True):
        st.header("📊 Deep Dive: AI Classification Trends")
        classification_trends_content(classifications_df)
    # --- 3.5. Life Stage Trends Container (New Section) ---
    with st.container(border=True):
        life_stage_trend_content(classifications_df) 
    # --- 4. Health Trends Container (Disease/Defect) ---
    with st.container(border=True):   
        disease_defect_by_species_content(classifications_df)

    
def life_stage_trend_content(classifications_df):
    """
    Analyzes and visualizes the trend of life stage classifications (Eggs, Larvae, Pupae, Butterfly) over time.
    """
    st.subheader("🗓️ Life Stage Classification Trend")
    
    # --- Data Processing for Stages ---
    
    # 1. Ensure timestamp is datetime and clean data
    if 'timestamp' not in classifications_df.columns:
        st.error("Missing 'timestamp' column for trend analysis.")
        return
        
    stage_df = classifications_df.copy()
    stage_df['timestamp'] = pd.to_datetime(stage_df['timestamp'], errors='coerce')
    stage_df = stage_df.dropna(subset=['timestamp'])

    # 2. Filter for relevant analysis types that include stage prediction
    relevant_analyses = ["Complete Analysis (All Models)", "Lifecycle Stage"]
    stage_df = stage_df[stage_df['analysis_type'].isin(relevant_analyses)]
    
    # 3. Filter out rows where predicted_stage is empty or not applicable (e.g., if model didn't predict)
    stage_df = stage_df[stage_df['predicted_stage'].notna() & (stage_df['predicted_stage'] != "")]

    if stage_df.empty:
        st.info("No life stage classification data available to plot trends.")
        return

    # 4. Group by week and predicted stage to get counts
    stage_df['week'] = stage_df['timestamp'].dt.to_period('W').astype(str)
    
    weekly_stages = stage_df.groupby(['week', 'predicted_stage']).size().reset_index(name='Stage Count')
    weekly_stages.rename(columns={'predicted_stage': 'Life Stage'}, inplace=True)
    
    # --- Visualization ---

    fig = px.line(
        weekly_stages,
        x='week',
        y='Stage Count',
        color='Life Stage',
        title="Weekly Classification Count of Life Stages",
        markers=True,
        height=450,
        labels={'week': 'Week of Year', 'Stage Count': 'Number of Classifications'}
    )
    fig.update_layout(template="seaborn", margin=dict(t=50, b=0, l=0, r=0))
    st.plotly_chart(fig, use_container_width=True)

def disease_defect_by_species_content(classifications_df):
    """
    Analyzes and visualizes the frequency of larval diseases and pupae defects
    grouped by predicted species.
    """
    st.subheader("🐛 Health Trends: Diseases & Defects by Species")
    
    # --- 1. Filter Data for Relevant Columns (Species, Disease, Defect) ---
    # We only care about rows where a species was identified (predicted_species != "")
    health_df = classifications_df[
        (classifications_df['predicted_species'] != "")
    ].copy()

    if health_df.empty:
        st.info("No classification data with species predictions found for health analysis.")
        return

    col1, col2 = st.columns(2)

    # --- 2. Larval Diseases by Species ---
    with col1:
        st.markdown("##### Larval Diseases Count by Species")
        
        # Filter for rows where a disease other than 'Healthy' was predicted
        disease_count_df = health_df[
            (health_df['predicted_disease'] != "") & 
            (health_df['predicted_disease'] != "Healthy")
        ].copy()
        
        if not disease_count_df.empty:
            # Group by species and disease type, then count
            disease_pivot = disease_count_df.groupby(['predicted_species', 'predicted_disease']).size().reset_index(name='Disease Count')
            
            # Create a stacked bar chart
            fig_disease = px.bar(
                disease_pivot,
                x='predicted_species',
                y='Disease Count',
                color='predicted_disease',
                title='Total Larval Diseases Detected per Species',
                height=450,
                labels={'predicted_species': 'Species', 'predicted_disease': 'Disease Type'}
            )
            fig_disease.update_layout(xaxis={'categoryorder':'total descending'}, margin=dict(t=50, b=0, l=0, r=0))
            st.plotly_chart(fig_disease, use_container_width=True)
        else:
            st.success("No non-healthy larval diseases detected with a species prediction.")

    # --- 3. Pupae Defects by Species ---
    with col2:
        st.markdown("##### Pupae Defects Count by Species")

        # Filter for rows where a defect other than 'Healthy Pupae' was predicted
        defect_count_df = health_df[
            (health_df['predicted_defect'] != "") & 
            (health_df['predicted_defect'] != "Healthy Pupae")
        ].copy()

        if not defect_count_df.empty:
            # Group by species and defect type, then count
            defect_pivot = defect_count_df.groupby(['predicted_species', 'predicted_defect']).size().reset_index(name='Defect Count')

            # Create a stacked bar chart
            fig_defect = px.bar(
                defect_pivot,
                x='predicted_species',
                y='Defect Count',
                color='predicted_defect',
                title='Total Pupae Defects Detected per Species',
                height=450,
                labels={'predicted_species': 'Species', 'predicted_defect': 'Defect Type'}
            )
            fig_defect.update_layout(xaxis={'categoryorder':'total descending'}, margin=dict(t=50, b=0, l=0, r=0))
            st.plotly_chart(fig_defect, use_container_width=True)
        else:
            st.success("No non-healthy pupae defects detected with a species prediction.")

def classification_trends_content(classifications_df):
    """
    Visualize AI classification trends over time.
    This function handles the logic for filters and charts.
    """
    
    # --- Data Processing for Trends ---
    if 'timestamp' in classifications_df.columns:
        classifications_df['timestamp'] = pd.to_datetime(classifications_df['timestamp'], errors='coerce')
        classifications_df = classifications_df.dropna(subset=['timestamp'])
    else:
        st.error("Missing 'timestamp' column for trend analysis.")
        return

    # Filter out non-species classifications for the main scatter plot
    species_df = classifications_df[classifications_df['predicted_species'].notna() & (classifications_df['predicted_species'] != "")]

    # --- Sidebar Filters (Refactored for clarity and proper placement) ---
    st.sidebar.header("🔍 Filter AI Data")
    filtered_df = species_df.copy()
    
    with st.sidebar.expander("Apply Filters", expanded=True):
        
        # Filter for User
        if 'user' in filtered_df.columns and not filtered_df['user'].empty:
            user_filter = st.multiselect(
                "Select User(s)",
                filtered_df['user'].unique(),
                default=filtered_df['user'].unique()
            )
            filtered_df = filtered_df[filtered_df['user'].isin(user_filter)]
        elif 'user' not in filtered_df.columns:
             st.info("No 'user' column found for filtering.")

        # Filter for Analysis Type
        if 'analysis_type' in filtered_df.columns and not filtered_df['analysis_type'].empty:
            analysis_filter = st.multiselect(
                "Select Analysis Type(s)",
                filtered_df['analysis_type'].unique(),
                # Only include Complete Analysis and Species Identification by default 
                # as the chart only plots Species data.
                default=[a for a in filtered_df['analysis_type'].unique() if a in ["Complete Analysis (All Models)", "Species Identification"]]
            )
            filtered_df = filtered_df[filtered_df['analysis_type'].isin(analysis_filter)]
        elif 'analysis_type' not in filtered_df.columns:
            st.info("No 'analysis_type' column found for filtering.")


    # --- Chart 1: Species Over Time (Scatter Plot) ---
    st.subheader("Species Predictions Over Time")
    
    if not filtered_df.empty:
        fig = px.scatter(
            filtered_df,
            x='timestamp',
            y='predicted_species',
            size='species_confidence',
            color='user',
            hover_data=['analysis_type', 'species_confidence'],
            title="Species Classification Trend by User",
            height=500
        )
        fig.update_layout(template="seaborn", margin=dict(t=50, b=0, l=0, r=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No species data available for selected filters.")

    # --- Chart 2: Optional Confidence Trend (Line Plot) ---
    st.markdown("---")
    if st.checkbox("Show Average Species Confidence Trend"):
        
        conf_df = filtered_df.copy()
        if not conf_df.empty:
            st.subheader("Species Confidence Trend")
            # Group data by week and predicted species
            conf_df['week'] = conf_df['timestamp'].dt.to_period('W').astype(str)
            
            weekly_confidence = conf_df.groupby(['week', 'predicted_species'])['species_confidence'].mean().reset_index()
            weekly_confidence.rename(columns={'species_confidence': 'Average Confidence'}, inplace=True)
            
            fig2 = px.line(
                weekly_confidence,
                x='week',
                y='Average Confidence',
                color='predicted_species',
                title="Weekly Average Species Confidence",
                markers=True,
                height=400
            )
            fig2.update_layout(template="seaborn", margin=dict(t=50, b=0, l=0, r=0))
            st.plotly_chart(fig2, use_container_width=True)
        else:
             st.info("Filter selection is too narrow to plot confidence trend.")

# This is the entry point for the Streamlit app
if __name__ == "__main__":
    dashboard_app()