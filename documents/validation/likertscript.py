"""
author: Benoît Duhoux
version: 01/2019
"""
import altair as alt

"""
Divergent stacked bar
"""

dsb_source = alt.pd.DataFrame(
    [
{'question': 'Je comprends les tâches', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je comprends les tâches', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0}, 
{'question': 'Je comprends les tâches', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': 0}, 
{'question': 'Je comprends les tâches', 'type': 4, 'value': 7.0, 'percentage': 77.7778, 'percentage_start': 0, 'percentage_end': 77.7778}, 
{'question': 'Je comprends les tâches', 'type': 5, 'value': 2.0, 'percentage': 22.2222, 'percentage_start': 77.7779, 'percentage_end': 100}, 

{'question': 'Je comprends le contexte', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je comprends le contexte', 'type': 2, 'value': 1.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -11.1111}, 
{'question': 'Je comprends le contexte', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': 0}, 
{'question': 'Je comprends le contexte', 'type': 4, 'value': 6.0, 'percentage': 66.6666, 'percentage_start': 0, 'percentage_end': 66.6666}, 
{'question': 'Je comprends le contexte', 'type': 5, 'value': 2.0, 'percentage': 22.2222, 'percentage_start': 66.6666, 'percentage_end': 88.8888},

{'question': 'Je comprends l\'utilité', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je comprends l\'utilité', 'type': 2, 'value': 1.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -11.1111}, 
{'question': 'Je comprends l\'utilité', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': 0}, 
{'question': 'Je comprends l\'utilité', 'type': 4, 'value': 5.0, 'percentage': 55.5555, 'percentage_start': 0, 'percentage_end': 55.5555}, 
{'question': 'Je comprends l\'utilité', 'type': 5, 'value': 3.0, 'percentage': 33.3333, 'percentage_start': 55.5555, 'percentage_end': 88.88888},

{'question': 'Je comprends les contrôles', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je comprends les contrôles', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0}, 
{'question': 'Je comprends les contrôles', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': 0}, 
{'question': 'Je comprends les contrôles', 'type': 4, 'value': 5.0, 'percentage': 88.8888, 'percentage_start': 0, 'percentage_end': 88.8888}, 
{'question': 'Je comprends les contrôles', 'type': 5, 'value': 3.0, 'percentage': 33.3333, 'percentage_start': 88.8888, 'percentage_end': 100.0},

{'question': 'Je sais où cliquer', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je sais où cliquer', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -33.3333, 'percentage_end': -11.1111}, 
{'question': 'Je sais où cliquer', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -11.11115, 'percentage_end': 11.1111}, 
{'question': 'Je sais où cliquer', 'type': 4, 'value': 5.0, 'percentage': 62.5, 'percentage_start': 11.1111, 'percentage_end': 66.6666}, 
{'question': 'Je sais où cliquer', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 0.0, 'percentage_end': 0.0},

{'question': 'Je peux réaliser les tâches facilement', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je peux réaliser les tâches facilement', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0.0, 'percentage_end': -0.0}, 
{'question': 'Je peux réaliser les tâches facilement', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -11.1111, 'percentage_end': 11.1111}, 
{'question': 'Je peux réaliser les tâches facilement', 'type': 4, 'value': 5.0, 'percentage': 62.5, 'percentage_start': 11.1111, 'percentage_end': 77.7777}, 
{'question': 'Je peux réaliser les tâches facilement', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 77.7777, 'percentage_end': 88.88888},

{'question': 'Je peux réaliser les tâches rapidement', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je peux réaliser les tâches rapidement', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -16.6666, 'percentage_end': -5.5555}, 
{'question': 'Je peux réaliser les tâches rapidement', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -5.5555, 'percentage_end': 5.5555}, 
{'question': 'Je peux réaliser les tâches rapidement', 'type': 4, 'value': 5.0, 'percentage': 62.5, 'percentage_start': 5.5555, 'percentage_end': 72.7777}, 
{'question': 'Je peux réaliser les tâches rapidement', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 72.7777, 'percentage_end': 83.88888},

{'question': 'Je comprends les données', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je comprends les données', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -11.1111, 'percentage_end': -0.0}, 
{'question': 'Je comprends les données', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0.0, 'percentage_end': 0.0}, 
{'question': 'Je comprends les données', 'type': 4, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 0.0, 'percentage_end': 55.5555}, 
{'question': 'Je comprends les données', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 55.55555, 'percentage_end': 88.88888},

{'question': 'L\'interface est adaptée', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'L\'interface est adaptée', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -16.6666, 'percentage_end': -5.5555}, 
{'question': 'L\'interface est adaptée', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -5.5555, 'percentage_end': 5.5555}, 
{'question': 'L\'interface est adaptée', 'type': 4, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 5.5555, 'percentage_end': 71.6666}, 
{'question': 'L\'interface est adaptée', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 71.6666, 'percentage_end': 82.7777},

{'question': 'Je me repère facilement', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'Je me repère facilement', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -38.8888, 'percentage_end': -5.5555}, 
{'question': 'Je me repère facilement', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -5.5555, 'percentage_end': 5.5555}, 
{'question': 'Je me repère facilement', 'type': 4, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 5.5555, 'percentage_end': 49.9999}, 
{'question': 'Je me repère facilement', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 49.9999, 'percentage_end': 61.1111},

{'question': 'J\'aime les couleurs', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'J\'aime les couleurs', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0}, 
{'question': 'J\'aime les couleurs', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -25.252525, 'percentage_end': 25.252525}, 
{'question': 'J\'aime les couleurs', 'type': 4, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 25.252525, 'percentage_end': 59}, 
{'question': 'J\'aime les couleurs', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 59, 'percentage_end': 71.1111},

{'question': 'J\'aime les images', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0}, 
{'question': 'J\'aime les images', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0}, 
{'question': 'J\'aime les images', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -25.252525, 'percentage_end': 25.252525}, 
{'question': 'J\'aime les images', 'type': 4, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 25.252525, 'percentage_end': 71.11111}, 
{'question': 'J\'aime les images', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 0.0, 'percentage_end': 0.0},

{'question': 'L\'agencement me convient', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -38.8888, 'percentage_end': -27.7777}, 
{'question': 'L\'agencement me convient', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -27.7777, 'percentage_end': -16.6666}, 
{'question': 'L\'agencement me convient', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -16.6666, 'percentage_end': 16.6666}, 
{'question': 'L\'agencement me convient', 'type': 4, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 16.6666, 'percentage_end': 61}, 
{'question': 'L\'agencement me convient', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 0.0, 'percentage_end': 0.0},

{'question': 'L\'esthétique générale me convient', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0}, 
{'question': 'L\'esthétique générale me convient', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0}, 
{'question': 'L\'esthétique générale me convient', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -11.1111, 'percentage_end': 11.1111}, 
{'question': 'L\'esthétique générale me convient', 'type': 4, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 11.1111, 'percentage_end': 66.6666}, 
{'question': 'L\'esthétique générale me convient', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 66.6666, 'percentage_end': 88.8888},

])

dsb = alt.Chart(dsb_source).mark_bar().encode(
        x  = alt.X('percentage_start:Q',  
                   scale=alt.Scale(domain = (-100, 100))
                  ),
        x2 = alt.X('percentage_end:Q'),
        y  = alt.Y('question:N', 
                   axis = alt.Axis(title     = 'Questions',
                                   offset    = 5,
                                   ticks     = False,
                                   minExtent = 60,
                                   domain    = False
                                  ),
                   sort = [
                       'Programming in general', 
                       'Object-oriented programming',
                       'Feature Modelling',
                       'Ruby programming language',
                       'Context-oriented programming',
                       'Our feature context approach'
                   ]
                  ),
        color = alt.Color('type:N',
                          #legend = alt.Legend( title = 'Possible responses'),
                          legend = None,
                          scale = alt.Scale(
                              domain = [1, 2, 3, 4, 5],
                              range  = ["#c30d24", "#f3a583", "#cccccc", "#94c6da", "#1770ab"]
                          )
                         )
)

neutral_source = alt.pd.DataFrame({
    'neutral': [0],
    'neutral': [0]
})

neutral = alt.Chart(neutral_source).mark_rule(color = 'black').encode(
            x = alt.X('neutral:Q')
)

full_dsb = (dsb + neutral).properties(
    width=550,
    height=351
)

"""
Frequencies bar charts
"""

questions = [
   'Programming in general', 
   'Object-oriented programming',
   'Feature Modelling',
   'Ruby programming language',
   'Context-oriented programming',
   'Our feature context approach'
]

frequencies = {
    'Feature Modelling': alt.pd.DataFrame(
        {
            'rating': [1, 2, 3, 4, 5],
            'frequencies': [2, 19, 8, 4, 0]
        }
    ),
    'Programming in general': alt.pd.DataFrame(
        {
            'rating': [1, 2, 3, 4, 5],
            'frequencies': [0, 5, 12, 13, 3]
        }
    ),
    'Object-oriented programming': alt.pd.DataFrame(
        {
            'rating': [1, 2, 3, 4, 5],
            'frequencies': [0, 4, 11, 15, 3]
        }
    ),
    
    'Ruby programming language': alt.pd.DataFrame(
        {
            'rating': [1, 2, 3, 4, 5],
            'frequencies': [23, 8, 1, 1, 0]
        }
    ),
    'Context-oriented programming': alt.pd.DataFrame(
        {
            'rating': [1, 2, 3, 4, 5],
            'frequencies': [13, 10, 6, 4, 0]
        }
    ),
    'Our feature context approach': alt.pd.DataFrame(
        {
            'rating': [1, 2, 3, 4, 5],
            'frequencies': [9, 15, 7, 2, 0]
        }
    )
}

frequencies_chart = None

for question in reversed(questions):
    x_axis = alt.Axis(title=None, labels=False, ticks=False)
    if frequencies_chart == None:
        x_axis = alt.Axis()
    
    chart = alt.Chart(frequencies[question]).mark_bar().encode(
        x=alt.X("rating:Q", scale=alt.Scale(domain = (1, 5)), axis=x_axis),
        y=alt.Y("frequencies:Q", axis=None)
    ).properties(height=38, width=200)
    
    text = chart.mark_text(
        align='left',
        baseline='top',
        dx=5,
        dy=1,
     ).encode(
        text='frequencies:Q'
    )
    
    if frequencies_chart == None:
        frequencies_chart = chart + text
    else:
        frequencies_chart = (chart + text) & frequencies_chart

frequencies_chart.save('test.html')
dsb.save('test2.html')

"""
Complete graph
"""
full_dsb | frequencies_chart
