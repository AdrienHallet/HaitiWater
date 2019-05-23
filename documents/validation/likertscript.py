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
{'question': 'Je comprends les tâches', 'type': 4, 'value': 12.0, 'percentage': 60, 'percentage_start': 0, 'percentage_end': 60},
{'question': 'Je comprends les tâches', 'type': 5, 'value': 8.0, 'percentage': 40, 'percentage_start': 60, 'percentage_end': 100},

{'question': 'Je comprends le contexte', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'Je comprends le contexte', 'type': 2, 'value': 1.0, 'percentage': 5.0, 'percentage_start': -2.5, 'percentage_end': -7.5},
{'question': 'Je comprends le contexte', 'type': 3, 'value': 1.0, 'percentage': 5.0, 'percentage_start': -2.5, 'percentage_end': 2.5},
{'question': 'Je comprends le contexte', 'type': 4, 'value': 8.0, 'percentage': 40.0, 'percentage_start': 2.5, 'percentage_end': 42.5},
{'question': 'Je comprends le contexte', 'type': 5, 'value': 10.0, 'percentage': 50.0, 'percentage_start': 42.5, 'percentage_end': 92.5},

{'question': 'Je comprends l\'utilité', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'Je comprends l\'utilité', 'type': 2, 'value': 1.0, 'percentage': 5.0, 'percentage_start': -2.5, 'percentage_end': -7.5},
{'question': 'Je comprends l\'utilité', 'type': 3, 'value': 1.0, 'percentage': 5.0, 'percentage_start': -2.5, 'percentage_end': 2.5},
{'question': 'Je comprends l\'utilité', 'type': 4, 'value': 7.0, 'percentage': 35.0, 'percentage_start': 2.5, 'percentage_end': 37.5},
{'question': 'Je comprends l\'utilité', 'type': 5, 'value': 11.0, 'percentage': 55.0, 'percentage_start': 37.5, 'percentage_end': 92.5},

{'question': 'Je comprends les contrôles', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'Je comprends les contrôles', 'type': 2, 'value': 1.0, 'percentage': 5.0, 'percentage_start': -5, 'percentage_end': -0},
{'question': 'Je comprends les contrôles', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': 0},
{'question': 'Je comprends les contrôles', 'type': 4, 'value': 17.0, 'percentage': 85.0, 'percentage_start': 0, 'percentage_end': 85.0},
{'question': 'Je comprends les contrôles', 'type': 5, 'value': 2.0, 'percentage': 10.0, 'percentage_start': 85.0, 'percentage_end': 95},

{'question': 'Je sais où cliquer', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'Je sais où cliquer', 'type': 2, 'value': 2.0, 'percentage': 10.0, 'percentage_start': -30, 'percentage_end': -20},
{'question': 'Je sais où cliquer', 'type': 3, 'value': 8.0, 'percentage': 40.0, 'percentage_start': -20.0, 'percentage_end': 20.0},
{'question': 'Je sais où cliquer', 'type': 4, 'value': 8.0, 'percentage': 40.0, 'percentage_start': 20, 'percentage_end': 70},
{'question': 'Je sais où cliquer', 'type': 5, 'value': 2.0, 'percentage': 10.0, 'percentage_start': 70, 'percentage_end': 80},

{'question': 'Je peux réaliser les tâches facilement', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'Je peux réaliser les tâches facilement', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0.0, 'percentage_end': -0.0},
{'question': 'Je peux réaliser les tâches facilement', 'type': 3, 'value': 6.0, 'percentage': 30.0, 'percentage_start': -15, 'percentage_end': 15},
{'question': 'Je peux réaliser les tâches facilement', 'type': 4, 'value': 10.0, 'percentage': 50, 'percentage_start': 15, 'percentage_end': 65},
{'question': 'Je peux réaliser les tâches facilement', 'type': 5, 'value': 4.0, 'percentage': 20, 'percentage_start': 65, 'percentage_end': 85},

{'question': 'Je peux réaliser les tâches rapidement', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'Je peux réaliser les tâches rapidement', 'type': 2, 'value': 1.0, 'percentage': 5.0, 'percentage_start': -17.5, 'percentage_end': -12.5},
{'question': 'Je peux réaliser les tâches rapidement', 'type': 3, 'value': 5.0, 'percentage': 25.0, 'percentage_start': -12.5, 'percentage_end': 12.5},
{'question': 'Je peux réaliser les tâches rapidement', 'type': 4, 'value': 12.0, 'percentage': 60.0, 'percentage_start': 12.5, 'percentage_end': 62.5},
{'question': 'Je peux réaliser les tâches rapidement', 'type': 5, 'value': 2.0, 'percentage': 10.0, 'percentage_start': 62.5, 'percentage_end': 72.5},

{'question': 'Je comprends les données', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'Je comprends les données', 'type': 2, 'value': 1.0, 'percentage': 5.0, 'percentage_start': -7.5, 'percentage_end': -2.5},
{'question': 'Je comprends les données', 'type': 3, 'value': 1.0, 'percentage': 5.0, 'percentage_start': -2.5, 'percentage_end': 2.5},
{'question': 'Je comprends les données', 'type': 4, 'value': 9.0, 'percentage': 45.0, 'percentage_start': 2.5, 'percentage_end': 47.5},
{'question': 'Je comprends les données', 'type': 5, 'value': 9.0, 'percentage': 45.0, 'percentage_start': 47.5, 'percentage_end': 92.5},

{'question': 'L\'interface est adaptée', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'L\'interface est adaptée', 'type': 2, 'value': 3.0, 'percentage': 0.0, 'percentage_start': -30, 'percentage_end': -15},
{'question': 'L\'interface est adaptée', 'type': 3, 'value': 6.0, 'percentage': 0.0, 'percentage_start': -15, 'percentage_end': 15},
{'question': 'L\'interface est adaptée', 'type': 4, 'value': 8.0, 'percentage': 0.0, 'percentage_start': 15, 'percentage_end': 55},
{'question': 'L\'interface est adaptée', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 55, 'percentage_end': 70},

{'question': 'Je me repère facilement', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'Je me repère facilement', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -38.8888, 'percentage_end': -5.5555},
{'question': 'Je me repère facilement', 'type': 3, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -5.5555, 'percentage_end': 5.5555},
{'question': 'Je me repère facilement', 'type': 4, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 5.5555, 'percentage_end': 49.9999},
{'question': 'Je me repère facilement', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 49.9999, 'percentage_end': 61.1111},

{'question': 'J\'aime les couleurs', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'J\'aime les couleurs', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0},
{'question': 'J\'aime les couleurs', 'type': 3, 'value': 5.0, 'percentage': 0.0, 'percentage_start': -12.5, 'percentage_end': 12.5},
{'question': 'J\'aime les couleurs', 'type': 4, 'value': 7.0, 'percentage': 0.0, 'percentage_start': 12.5, 'percentage_end': 57.5},
{'question': 'J\'aime les couleurs', 'type': 5, 'value': 8.0, 'percentage': 0.0, 'percentage_start': 57.5, 'percentage_end': 97.5},

{'question': 'J\'aime les images', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': 0, 'percentage_end': -0},
{'question': 'J\'aime les images', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0},
{'question': 'J\'aime les images', 'type': 3, 'value': 9.0, 'percentage': 0.0, 'percentage_start': -22.5, 'percentage_end': 22.5},
{'question': 'J\'aime les images', 'type': 4, 'value': 8.0, 'percentage': 0.0, 'percentage_start': 22.5, 'percentage_end': 62.5},
{'question': 'J\'aime les images', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 62.5, 'percentage_end': 77.5},

{'question': 'L\'agencement me convient', 'type': 1, 'value': 1.0, 'percentage': 0.0, 'percentage_start': -25, 'percentage_end': -20},
{'question': 'L\'agencement me convient', 'type': 2, 'value': 2.0, 'percentage': 0.0, 'percentage_start': -20, 'percentage_end': -10},
{'question': 'L\'agencement me convient', 'type': 3, 'value': 4.0, 'percentage': 0.0, 'percentage_start': -10, 'percentage_end': 10},
{'question': 'L\'agencement me convient', 'type': 4, 'value': 10.0, 'percentage': 0.0, 'percentage_start': 10, 'percentage_end': 60},
{'question': 'L\'agencement me convient', 'type': 5, 'value': 3.0, 'percentage': 0.0, 'percentage_start': 60, 'percentage_end': 75},

{'question': 'L\'esthétique générale me convient', 'type': 1, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0},
{'question': 'L\'esthétique générale me convient', 'type': 2, 'value': 0.0, 'percentage': 0.0, 'percentage_start': -0, 'percentage_end': -0},
{'question': 'L\'esthétique générale me convient', 'type': 3, 'value': 4.0, 'percentage': 0.0, 'percentage_start': -10, 'percentage_end': 10},
{'question': 'L\'esthétique générale me convient', 'type': 4, 'value': 11.0, 'percentage': 0.0, 'percentage_start': 10, 'percentage_end': 65},
{'question': 'L\'esthétique générale me convient', 'type': 5, 'value': 5.0, 'percentage': 0.0, 'percentage_start': 65, 'percentage_end': 90},

])

dsb = alt.Chart(dsb_source).mark_bar().encode(
        x  = alt.X('percentage_start:Q',
                   scale=alt.Scale(domain = (-100, 100))
                  ),
        x2 = alt.X('percentage_end:Q'),
        y  = alt.Y('question:N',
                   axis = alt.Axis(title     = '',
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
