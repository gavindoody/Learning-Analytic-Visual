import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

np.random.seed(42)

num_students = 50

student_ids = ['Student' + str(i) for i in range(1, num_students+1)]

scores = np.random.randint(50, 100, size=num_students)

completion_times = np.random.randint(30, 180, size=num_students)

data = pd.DataFrame({
    'Student ID': student_ids,
    'Score': scores,
    'Completion Time (min)': completion_times
})

plt.figure(figsize=(10, 6))
plt.bar(data['Student ID'], data['Score'], color='skyblue')
plt.xlabel('Student ID')
plt.ylabel('Score')
plt.title('Student Scores on Assignment')
plt.xticks(rotation=45, ha='right') 
plt.tight_layout()
plt.show()

fig = px.scatter(data, x='Completion Time (min)', y='Score', hover_name='Student ID', title='Student Performance on Assignment')
fig.update_traces(marker=dict(size=12, opacity=0.8))
fig.show()


import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Student Learning Analytics Dashboard"),
    
    html.Div([
        html.H2("Student Scores"),
        dcc.Graph(
            id='score-graph'
        )
    ]),
    
    html.Div([
        html.H2("Completion Time vs. Score"),
        dcc.Graph(
            id='scatter-plot'
        )
    ])
])

@app.callback(
    Output('score-graph', 'figure'),
    Input('scatter-plot', 'hoverData')
)
def update_score_graph(hoverData):
    student_id = hoverData['points'][0]['hovertext'] if hoverData else data['Student ID'].iloc[0]
    student_data = data[data['Student ID'] == student_id]
    
    trace = go.Bar(x=student_data['Student ID'], y=student_data['Score'], name='Score', marker=dict(color='skyblue'))
    
    return {
        'data': [trace],
        'layout': go.Layout(
            title=f"Score for Student: {student_id}",
            xaxis={'title': 'Student ID'},
            yaxis={'title': 'Score'}
        )
    }

if __name__ == '__main__':
    app.run_server(debug=True)
