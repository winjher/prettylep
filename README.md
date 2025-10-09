#PRETTYLEP
"Species Identified"
"Life Stages Classified"
"Larval Diseases Classified"
"Pupae Defects Classified"
Columns in df: Index(['timestamp', 'analysis_type', 'user', 'predicted_species',
       'species_confidence', 'predicted_stage', 'stage_confidence',
       'predicted_disease', 'disease_confidence', 'predicted_defect',
       'defect_confidence'],
      dtype='object')
Columns in df: Index(['timestamp', 'analysis_type', 'user', 'predicted_species',
       'species_confidence', 'predicted_stage', 'stage_confidence',
       'predicted_disease', 'disease_confidence', 'predicted_defect',
       'defect_confidence'],
      dtype='object')
Columns in df: Index(['timestamp', 'analysis_type', 'user', 'predicted_species',
       'species_confidence', 'predicted_stage', 'stage_confidence',
       'predicted_disease', 'disease_confidence', 'predicted_defect',
       'defect_confidence'],
      dtype='object')
Columns in df: Index(['timestamp', 'analysis_type', 'user', 'predicted_species',
       'species_confidence', 'predicted_stage', 'stage_confidence',
       'predicted_disease', 'disease_confidence', 'predicted_defect',
       'defect_confidence'],
      dtype='object')

df=pd.read_csv("./ai_classifications.csv")
print("Columns in df:",df.columns)
fig = px.histogram(df, x="predicted_species", title="Species Classification Distribution", labels={"predicted_species": "Butterfly Species"}, color_discrete_sequence=['#636EFA'])
            st.plotly_chart(fig)

df=pd.read_csv("./ai_classifications.csv")
print("Columns in df:",df.columns)
fig = px.histogram(df, x="predicted_stage", title="Larval Diseases Classification Distribution", labels={"predicted_species": "Butterfly Species"}, color_discrete_sequence=['#636EFA'])
st.plotly_chart(fig)

df=pd.read_csv("./ai_classifications.csv")
print("Columns in df:",df.columns)
fig = px.histogram(df, x="predicted_defect", title="Pupae Defects Classification Distribution", labels={"predicted_species": "Butterfly Species"}, color_discrete_sequence=['#636EFA'])
st.plotly_chart(fig)

df=pd.read_csv("./ai_classifications.csv")
print("Columns in df:",df.columns)
fig = px.histogram(df, x="predicted_disease", title="Life Stages Classification Distribution", labels={"predicted_species": "Butterfly Species"}, color_discrete_sequence=['#636EFA'])
st.plotly_chart(fig)