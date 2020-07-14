import dash
import flask
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#external_css = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/css/materialize.min.css']


app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)
server=app.server

#----------------------------------------------------------------------------
df = pd.read_csv('final-data.csv')
tcases = pd.read_csv('daily cases.csv')
dfper = pd.read_csv('final-data-perage.csv')


#---------------------------------------------------------------------------
#---------------------
#functions
def retdata(val):

    if val == 'all':
        dff = df.copy()
        return dff
    if val == 'per':
        dff = dfper.copy()
        return dff


def Navbar():
    navbar = html.Div([
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Sentiments",
                            href="/page-1",
                            id="page-1-link",
                            style={
                                'text-color': 'white',
                                'font-size': '25px'
                            }),
                dbc.NavLink("Word cloud",
                            href="/page-2",
                            id="page-2-link",
                            style={
                                'text-color': 'white',
                                'font-size': '25px'
                            }),
                dbc.NavLink("Tweets",
                            href="/page-3",
                            id="page-3-link",
                            style={
                                'text-color': 'white',
                                'font-size': '25px'
                            }),
            ],
            brand="Covid-19 Twitter Analysis India",
            color="dark",
            dark=True,
            sticky='top',
        ),
        dbc.Container(id="page-content", className="pt-4", fluid=True)
    ])
    return navbar


nav = Navbar()

app.layout = html.Div([nav])


@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]


@app.callback(Output('date-line', 'children'), [Input('tabs', 'value')])
def render_content(tab):

    if tab == 'tab-1':
        dff = retdata('all')
        col = list(dff.columns)
        col.pop(0)
        col.pop(-1)
        fig = px.line(dff, x="date", y=col)
        fig.add_shape(type="line",
                      line_color="salmon",
                      line_width=3,
                      opacity=1,
                      line_dash="dot",
                      x0="24-Mar",
                      x1="24-Mar",
                      y0=0,
                      y1=300)

        fig.add_annotation(text="Lockdown - 1",
                           x="24-Mar",
                           y=300,
                           arrowhead=1,
                           showarrow=True)
        fig.add_shape(type="line",
                      line_color="salmon",
                      line_width=3,
                      opacity=1,
                      line_dash="dot",
                      x0="15-Apr",
                      x1="15-Apr",
                      y0=0,
                      y1=300)

        fig.add_annotation(text="Lockdown - 2",
                           x="15-Apr",
                           y=300,
                           arrowhead=1,
                           showarrow=True)
        fig.add_shape(type="line",
                      line_color="salmon",
                      line_width=3,
                      opacity=1,
                      line_dash="dot",
                      x0="04-May",
                      x1="04-May",
                      y0=0,
                      y1=300)

        fig.add_annotation(text="Lockdown - 3",
                           x="04-May",
                           y=300,
                           arrowhead=1,
                           showarrow=True)
        fig.add_shape(type="line",
                      line_color="salmon",
                      line_width=3,
                      opacity=1,
                      line_dash="dot",
                      x0="18-May",
                      x1="18-May",
                      y0=0,
                      y1=300)

        fig.add_annotation(text="Lockdown - 4",
                           x="18-May",
                           y=300,
                           arrowhead=1,
                           showarrow=True)
        fig.update_layout(legend_title_text='Sentiment',
                          yaxis_title='No.of Tweets')
        fig.update_xaxes(nticks=20)
        
        writ1=html.Div([
            html.P(style={'font-size':'18px'},children=[' 1. After studying the above Graph, We notice that the no.of tweets are significantly increasing right before every lockdown. This is because the Engagement of the users starts increasing right after the Announcement is made, i.e 2-3 days prior the lockdown date.']),
            html.P(style={'font-size':'18px'},children=[' 2. Similarly ,sentiments such as Anger ,Confidence ,Sadness and Analytics  increased on announcements from the government.']),
            html.P(style={'font-size':'18px'},children=[' 3. We also observe that after the commencement of the lockdown, engagement dip for a while, this is seen significantly after the 3rd lockdown showing a sign of exhaustion among the public.']),
            html.P(style={'font-size':'18px'},children=[' 4. Post 4th lockdown, we see gradual decrease in No.of Tweets, due to less talk among the public.']), 
            ])
        
        cardcont =[
                dbc.CardHeader(html.H3('Findings :')),
                dbc.CardBody(writ1),
            ]
        cards = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(cardcont, color="dark", inverse=True))
                    ])
            ])
        
        return html.Div([dcc.Graph(id='fig1g',figure=fig),
        cards,    
        ])

    elif tab == 'tab-2':
        dff = retdata('per')
        datec = dff['date']
        analyg = dff['analytics']
        angg = dff['anger']
        confg = dff['confident']
        sadg = dff['sadness']
        fearg = dff['fear']
        joyg = dff['joy']

        fig = make_subplots(rows=2,
                            cols=3,
                            shared_yaxes=True,
                            subplot_titles=("Analytics", "Anger", "Confident",
                                            "Sadness", "Fear", "Joy"),
                            y_title='Sentiment Density %',x_title='Days')

        for i in range(1, 3):
            for j in range(1, 4):
                fig.add_shape(type="line",
                              line_color="dimgrey",
                              line_width=3,
                              opacity=1,
                              line_dash="dot",
                              x0="24-Mar",
                              x1="24-Mar",
                              y0=0,
                              y1=40,
                              row=i,
                              col=j)

                fig.add_annotation(text="Phase-1",
                                   x="24-Mar",
                                   y=40,
                                   arrowhead=1,
                                   showarrow=True,
                                   row=i,
                                   col=j)
                fig.add_shape(type="line",
                              line_color="dimgrey",
                              line_width=3,
                              opacity=1,
                              line_dash="dot",
                              x0="15-Apr",
                              x1="15-Apr",
                              y0=0,
                              y1=40,
                              row=i,
                              col=j)

                fig.add_annotation(text="Phase-2",
                                   x="15-Apr",
                                   y=40,
                                   arrowhead=1,
                                   showarrow=True,
                                   row=i,
                                   col=j)
                fig.add_shape(type="line",
                              line_color="dimgrey",
                              line_width=3,
                              opacity=1,
                              line_dash="dot",
                              x0="04-May",
                              x1="04-May",
                              y0=0,
                              y1=40,
                              row=i,
                              col=j)

                fig.add_annotation(text="Phase-3",
                                   x="04-May",
                                   y=40,
                                   arrowhead=1,
                                   showarrow=True,
                                   font=dict(size=10),
                                   row=i,
                                   col=j)
                fig.add_shape(type="line",
                              line_color="dimgrey",
                              line_width=3,
                              opacity=1,
                              line_dash="dot",
                              x0="18-May",
                              x1="18-May",
                              y0=0,
                              y1=40,
                              row=i,
                              col=j)

                fig.add_annotation(text="Phase-4",
                                   x="18-May",
                                   y=40,
                                   arrowhead=1,
                                   font=dict(size=10),
                                   showarrow=True,
                                   row=i,
                                   col=j)

        fig.add_trace(go.Scatter(opacity=0.2,
                                 x=datec,
                                 y=tcases['totper'],
                                 name='% increase in Covid Cases',
                                 line=dict(color='indianred'),
                                 fill='tozeroy'),
                      row=1,
                      col=1)
        fig.add_trace(go.Scatter(x=datec,
                                 y=analyg,
                                 name='Analytics',
                                 line=dict(color='blueviolet')),
                      row=1,
                      col=1)
        fig.add_trace(go.Scatter(opacity=0.2,
                                 x=datec,
                                 y=tcases['totper'],
                                 line=dict(color='indianred'),
                                 showlegend=False,
                                 fill='tozeroy'),
                      row=1,
                      col=2)
        fig.add_trace(go.Scatter(x=datec, y=angg, name='Angry'), row=1, col=2)

        fig.add_trace(go.Scatter(opacity=0.2,
                                 x=datec,
                                 y=tcases['totper'],
                                 line=dict(color='indianred'),
                                 showlegend=False,
                                 fill='tozeroy'),
                      row=1,
                      col=3)

        fig.add_trace(go.Scatter(x=datec, y=confg, name='Confident'),
                      row=1,
                      col=3)

        fig.add_trace(go.Scatter(opacity=0.2,
                                 x=datec,
                                 y=tcases['totper'],
                                 line=dict(color='indianred'),
                                 showlegend=False,
                                 fill='tozeroy'),
                      row=2,
                      col=1)

        fig.add_trace(go.Scatter(x=datec,
                                 y=sadg,
                                 name='Sadness',
                                 line=dict(color='cornflowerblue')),
                      row=2,
                      col=1)

        fig.add_trace(go.Scatter(opacity=0.2,
                                 x=datec,
                                 y=tcases['totper'],
                                 line=dict(color='indianred'),
                                 showlegend=False,
                                 fill='tozeroy'),
                      row=2,
                      col=2)

        fig.add_trace(go.Scatter(x=datec,
                                 y=fearg,
                                 name='Fear',
                                 line=dict(color='dimgray')),
                      row=2,
                      col=2)

        fig.add_trace(go.Scatter(opacity=0.2,
                                 x=datec,
                                 y=tcases['totper'],
                                 line=dict(color='indianred'),
                                 showlegend=False,
                                 fill='tozeroy'),
                      row=2,
                      col=3)

        fig.add_trace(go.Scatter(x=datec, y=joyg, name='Joy'), row=2, col=3)

        fig.update_layout(title_text="Multiple Sentiments")

        fig.update_xaxes(nticks=10)

        #fig.update_layout(showlegend=False)

        writ2=html.Div([
            html.P(style={'font-size':'18px'},children=[' -> Growth Rate =  ((No. of Cases on Present Day  - No. of cases on previous day) /(No. of Cases on Previous Day ))  * 100']),
            html.P(style={'font-size':'18px'},children=[' -> The above graph shows sentiment-wise variations with the percentage of rise in covid cases.']),
            html.P(style={'font-size':'18px'},children=[' -> Significant percentage of the Tweets are Analytical in Nature, An analytical tone indicates a persons reasoning and analytical attitude about things. An analytical tweet might be perceived as intellectual, rational, systematic, emotionless, or impersonal.']),
            html.P(style={'font-size':'18px'},children=[' -> We can see Serious Anger among the Public during the Lockdown, But we also see Notable Confidence with the Tweets . This Signifies the presence of People from Both the sides  i.e those embracing the Lockdown and also presence of those against the governments actions.']),
            html.P(style={'font-size':'18px'},children=[' -> Sentiments such as Sadness and Fear show similar trends among Users,which has gradually increased Over time.']),
            html.P(style={'font-size':'18px'},children=[' -> We also Observe tweets with Joy during these times,it mostly indicates the response to  Vaccine developments, appreciation for frontline workers ,government actions and also the Strong meme game of our country.']),
             
            ])
        
        cardcont =[
                dbc.CardHeader(html.H3('Findings :')),
                dbc.CardBody(writ2),
            ]
        cards = html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(cardcont, color="dark", outline=True))
                    ])
            ])
        
        return html.Div([dcc.Graph(id='fig1g',figure=fig),
        cards,    
        ])

    elif tab == 'tab-3':
        Sentimentclass = [
            'Analytics', 'Anger', 'Confident', 'Sadness', 'Fear', 'Joy'
        ]
        totalsent = [16644, 13098, 12511, 6141, 3839, 6394]
        colors = [
            'dimgrey', 'indianred', 'blueviolet', 'darkslategray',
            'mediumslateblue', 'lightseagreen'
        ]
        fig = px.bar(df,
                     color=Sentimentclass,
                     y=totalsent,
                     x=Sentimentclass,
                     text=totalsent,
                     color_discrete_sequence=colors)
        fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig.add_layout_image(
            dict(
                source="/assets/collage.png",
                #xref="paper",
                #yref="paper",
                x=1,
                y=0.8,
                sizex=0.5,
                sizey=0.5,
                xanchor="right",
                yanchor="bottom"))
        fig.update_layout(
            title_text="Comparison of Total Tweets of Respective Sentiments")
        fig.update_xaxes(title_text='Sentiment')
        fig.update_yaxes(title_text='Total tweets')
        
        return html.Div([dcc.Graph(id='fig3g',figure=fig)
        ])

    elif tab == 'tab-4':
        topics = [
            'lockdown', 'economy', 'migrants', 'unemployment', 'atmanirbhar',
            'unlock', 'vaccine', 'quarantine'
        ]
        tottweetstopics = [3755, 719, 1117, 770, 555, 290, 668, 700]
        colors = [
            'dimgrey', 'indianred', 'blueviolet', 'darkslategray',
            'mediumslateblue', 'lightseagreen', 'blue', 'yellow'
        ]

        fig4 = px.bar(df,
                      color=topics,
                      y=tottweetstopics,
                      x=topics,
                      text=tottweetstopics,
                      color_discrete_sequence=colors)
        fig4.update_layout(title_text="Number of Tweets Topic-Wise")
        fig4.update_traces(texttemplate='%{text:.2s}', textposition='outside')
        fig4.update_xaxes(title_text='Topics')
        fig4.update_yaxes(title_text='Number of Tweets')

        cards = html.Div(
            [
                dbc.Card(
                    dbc.CardBody(html.H4("Covid Related Trending Topics")),
                    className="mb-3",color='info',inverse=True,
                ),
            ]
        )
        
        return html.Div([cards,dcc.Graph(id='fig4g',figure=fig4)
        ])

    elif tab == 'tab-5':

        xlab = [
            'lockdown', 'atmanirbhar', 'economy', 'migrants', 'quarantine',
            'unemployment', 'unlock', 'vaccine'
        ]

        fig5 = go.Figure()
        fig5.add_trace(
            go.Bar(x=xlab,
                   y=[
                       0.081451664, 0.054615854, 0.098453408, 0.163425246,
                       0.058937143, 0.115937861, 0.05115, 0.059008982
                   ],
                   name='Negative',
                   marker_color='indianred'))

        fig5.add_trace(
            go.Bar(x=xlab,
                   y=[
                       0.079668708, 0.187534553, 0.097154381, 0.094118174,
                       0.09398, 0.121456647, 0.0754125, 0.097772455
                   ],
                   name='Positive',
                   marker_color='lightseagreen'))
        fig5.add_trace(
            go.Bar(x=xlab,
                   y=[
                       -0.033913422, 0.435397967, -0.121601113, -0.211934378,
                       0.104937, -0.106924422, 0.067030625, 0.149996856
                   ],
                   name='Compound',
                   marker_color='slateblue'))
        fig5.add_layout_image(
            dict(source="/assets/label.jpg",
                 x=1,
                 y=0.9,
                 sizex=0.5,
                 sizey=0.5,
                 xanchor="right",
                 yanchor="bottom"))

        fig5.update_layout(title_text='Topic-Wise Sentiment')
        fig5.update_xaxes(title_text='Topics')
        fig5.update_yaxes(title_text='Sentiment Value')

        cards = html.Div(
            [
                dbc.Card(
                    dbc.CardBody([html.H6("Negative -  Indicates How Negative the Tweet is ,with 1 being the most negative and 0 for least Negative."),
                    html.H6("Positive -  Indicates How Positive the Tweet is, with 1 being the most positive and 0 for least Positive."),
                    html.H6("Compound - Provides an Overall tweet Polarity of the Tweet , with 1 being Highly positive, -1 being Highly Negative, and 0 for Neutral.")]),
                    className="mb-3",color='light',
                ),
            ]
        )

        cards5 = html.Div(
            [
                dbc.Card(
                    dbc.CardBody([html.H6("-> The Above Graph Clearly Depicts the Overall Sentiment of the Users on These Topics."),
                    html.H6("-> 'AatmaNirbhar' is the name given to the covid relief package announced by PMO India, which has highly appreciated and accepted positively in twitter."),
                    html.H6("-> The people on twitter Raged on the 'Economy' , 'Unemployability' and 'Migrant' issues and expressed their Anger and Dissatisfaction on the Government."),
                    html.H6("-> 'Vaccine' and 'Unlock' Topics have received Good response and is Welcomed by people on Twitter.")]),
                    className="mb-3",color='dark',inverse=True,
                ),
            ]
        )

        return html.Div([cards,dcc.Graph(id='fig5g',figure=fig5),cards5
        ])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/page-1"]:
        pag1 = html.Div([
            html.H2(children='Covid19 Twitter Analysis India',
                    style={'text-align': 'center'}),
            dcc.Tabs(id="tabs",
                     value='tab-1',
                     children=[
                         dcc.Tab(label='Overall Statistics', value='tab-1'),
                         dcc.Tab(label='Sentiment Wise', value='tab-2'),
                         dcc.Tab(label='Total Sentiment Count', value='tab-3'),
                         dcc.Tab(label='Topic Wise', value='tab-4'),
                         dcc.Tab(label='Topic Wise - Sentiment', value='tab-5')
                     ]),
            html.Br(),
            #dcc.Graph(id='date-line'),
            html.Div(id='date-line')
            

        ])
        return pag1

    elif pathname == "/page-2":
        top_card = dbc.Card(
            [
                dbc.CardBody(
                    html.P("Most Frequent Words", className="text-center")),
                dbc.CardImg(src="/assets/Wordcloud.png", bottom=True),
            ],
            style={"width": "18rem"},
            className="w-75",
            color="dark",
            inverse=True,
        )
        cards = html.Div(dbc.Row(top_card, justify="center"))
        return html.P(cards)

    elif pathname == "/page-3":
        cards = html.Div([
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Analytics",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/analytics.jpg",
                                        bottom=True),
                        ],
                                 color='secondary',
                                 inverse=True)),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Angry",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/angry.jpg",
                                        bottom=True),
                        ],
                                 color="danger",
                                 inverse=True)
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Confident",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/confident.jpg",
                                        bottom=True),
                        ],
                                 style={'background-color': 'mediumpurple'},
                                 inverse=True)
                    ]),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Sadness", className="card-text")),
                            dbc.CardImg(src="/assets/cards/sad.jpg",
                                        bottom=True),
                        ],
                                 color="info",
                                 inverse=True)
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Fear",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/fear.jpg",
                                        bottom=True),
                        ],
                                 color="dark",
                                 inverse=True)
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Joy",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/joy.jpg",
                                        bottom=True),
                        ],
                                 color="success",
                                 inverse=True)
                    ]),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Analytics",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/analytics2.jpg",
                                        bottom=True),
                        ],
                                 color='secondary',
                                 inverse=True)),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Angry",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/angry2.jpg",
                                        bottom=True),
                        ],
                                 color="danger",
                                 inverse=True)
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Confident",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/confident2.jpg",
                                        bottom=True),
                        ],
                                 style={'background-color': 'mediumpurple'},
                                 inverse=True)
                    ]),
                ],
                className="mb-4",
            ),
            dbc.Row(
                [
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Sadness", className="card-text")),
                            dbc.CardImg(src="/assets/cards/sad2.jpg",
                                        bottom=True),
                        ],
                                 color="info",
                                 inverse=True)
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Fear",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/fear2.jpg",
                                        bottom=True),
                        ],
                                 color="dark",
                                 inverse=True)
                    ]),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardBody(
                                html.P("Joy",
                                       className="card-text",
                                       style={'font-size': '20px'})),
                            dbc.CardImg(src="/assets/cards/joy2.jpg",
                                        bottom=True),
                        ],
                                 color="success",
                                 inverse=True)
                    ]),
                ],
                className="mb-4",
            ),
        ])
        titlename = html.P("Some of Top Tweets and their Sentiment",
                           className="text-center",
                           style={
                               'font-family': 'Verdana',
                               'font-size': '30px'
                           })
        pag3 = html.Div([titlename, html.Br(), cards])
        return html.P(pag3)

    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron([
        html.H1("404: Not found", className="text-danger"),
        html.Hr(),
        html.P(f"The pathname {pathname} was not recognised..."),
    ])


if __name__ == '__main__':
    app.run_server(debug=True)