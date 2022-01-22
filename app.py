import pandas as pd
import dash                                
from dash import html
from dash import dcc
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc  
import plotly.express as px             
             
from datetime import date
import calendar
import numpy as np



vendas = pd.read_csv('vendas.csv')


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody(html.H2("Report Vendas 2021")) 
            ], color = "success", className='mb-2', style={'height':'18vh' }),            
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                            id='country-dd',
                            options=[{'label':'Sao Paulo','value':'Sao Paulo'},
                                    {'label':'Salvador','value':'Salvador'},
                                    {'label':'Rio de Janeiro', 'value':'Rio de Janeiro'},
                                    {'label':'Porto Alegre', 'value':'Porto Alegre'},
                                    {'label':'Brasilia','value':'Brasilia'},
                                    {'label':'Fortaleza','value':'Fortaleza'},
                                    {'label':'Curitiba','value':'Curitiba'}],                    
                            placeholder="Escolha uma cidade", 
                            clearable=True, 
                            className="dropdown",                                 
                        ),
                    ])
                ], color="success", style={'height':'18vh'}),
            ], width=3),
        dbc.Col([
             dbc.Card([
                dbc.CardBody([
                    dcc.Dropdown(
                            id='product-dd',
                            options=[{'label':'Casaco','value':'Casaco'},
                                     {'label':'Camiseta','value':'Camiseta'},
                                     {'label':'Sapato', 'value':'Sapato'},
                                     {'label':'Vestido', 'value':'Vestido'},
                                     {'label':'Sandalia','value':'Sandalia'},
                                     {'label':'Saia','value':'Saia'},
                                     {'label':'Bermuda','value':'Bermuda'},  
                                     {'label':'Pulseira', 'value':'Pulseira'},
                                     {'label':'Jaqueta','value':'Jaqueta'},
                                     {'label':'Tenis','value':'Tenis'},
                                     {'label':'Short','value':'Short'},
                                     {'label':'Chinelo','value':'Chinelo'},],                   
                            placeholder="Escolha um produto",
                            clearable=True, 
                            className="dropdown",
                        ),
                    ])
                ], color="success", style={'height':'18vh'}),
            ],width=3),
        dbc.Col([                    
            dbc.Card([
                dbc.CardBody( )
            ], color="success", style={'height':'18vh'}),
        ], width=2),
    ]
    ,className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Faturamento'),
                dbc.CardBody([
                    html.H3(id='content-connections', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Unidades Vendidas'),
                dbc.CardBody([
                    html.H3(id='content-companies', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Preço Médio'),
                dbc.CardBody([                    
                    html.H3(id='content-msg-in', children="000")
                ], style={'textAlign':'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Itens únicos'),
                dbc.CardBody([
                    html.H3(id='content-msg-out', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Qtd devoluções'),
                dbc.CardBody([
                    html.H3(id='content-reactions', children="000")
                ], style={'textAlign': 'center'})
            ]),
        ], width=2),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='major-cat', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='major-product', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
    dbc.Row([
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line_graph', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='tree_fig', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2'),
], fluid="True")


# Updating the 5 number cards ******************************************
@app.callback(
    Output('content-connections','children'),
    [Input('product-dd','value'),
     Input('country-dd','value'),
     ])

# Faturamento
def update_small_cards(input_product, input_country):
    
    vendasc = vendas.copy()
    if input_product:
        produto_filter = input_product
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter] 
     
    conctns_num = vendasc['Faturamento'].sum()
    return f'R$ {conctns_num:,}'


# Unidades vendidas
@app.callback(
    Output('content-companies','children'),
     [Input('country-dd','value'),
     Input('product-dd','value'),
     ])

def update_small_cards(input_country, input_product):
    vendasc = vendas.copy()
    if input_product:
        produto_filter = input_product
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter] 
    
    compns_num = vendasc['Quantidade Vendida'].sum()
    return compns_num

# Preco
@app.callback(
    Output('content-msg-in','children'),
    [Input('country-dd','value'),
     Input('product-dd','value'),
    ])

def update_small_cards(input_country, input_product):
    vendasc = vendas.copy()
    if input_product:
        produto_filter = input_product
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter] 
    
    in_num = round(vendasc['Preco'].mean(),2)
    return f"R$ {in_num:,}"
    
# Itens Unicos a venda
@app.callback(
    Output('content-msg-out','children'),
    [Input('country-dd','value'),
     Input('product-dd','value'),
     ])

def update_small_cards(input_country, input_product):
    vendasc = vendas.copy()
    if input_product:
        produto_filter = input_product
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]     
    out_num = vendasc['Produto'].nunique()
    return out_num

# Qtd Devolvida
@app.callback(
    Output('content-reactions','children'),
    [Input('country-dd','value'),
     Input('product-dd','value'),
     ])

def update_small_cards(input_country, input_product):
    vendasc = vendas.copy()
    if input_product:
        produto_filter = input_product
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]     
    reactns_num = vendasc['Produto'].nunique()
    return reactns_num
    




# Major Cat ***********************************************************
@app.callback(
    Output(component_id='major-cat', component_property='figure'),
    Input(component_id='country-dd', component_property='value'),
)

def update_plot(input_country):
    country_filter = 'Todas Cidades'
    vendasc = vendas.copy(deep=True)
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]
    
    ecom_bar_major_cat = vendasc.groupby('Produto')['Faturamento'].agg('sum').reset_index(name='Total')
    bar_fig_produto = px.bar(
    data_frame = ecom_bar_major_cat, 
    title = 'Faturamento total por produto', 
    x = 'Produto', 
    y='Total',    
    color = 'Produto', 
    text_auto=True, 
    labels = dict(Produto="", Total="Faturamento"))
    bar_fig_produto.update_layout(showlegend=False)
    return bar_fig_produto


# Line Graph ************************************************************
@app.callback(
    Output(component_id='line_graph', component_property='figure'),
    [Input(component_id='product-dd', component_property='value'),
     Input(component_id='country-dd', component_property='value')])

def update_plot(input_produto, input_country):
    produto_filter = 'Todos produtos'
    vendasc = vendas.copy(deep=True)
    if input_produto:
        produto_filter = input_produto
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]
    vendasg=vendasc.groupby(['Mes_Vendas_Num','Loja'])['Faturamento'].agg('sum').reset_index(name='Faturamento total')
    line_graph = px.line(
    data_frame = vendasg, 
    title = 'Faturamento total por Mês/Loja',
    x = 'Mes_Vendas_Num',
    y= 'Faturamento total', 
    color = 'Loja',
    labels = dict(Mes_Vendas_Num="", Faturamento_total= "Faturamento"))
    line_graph.update_xaxes(
    ticktext=["Janeiro","Fevereiro","Marco" ,"Abril","Maio" ,"Junho","Julho", "Agosto","Setembro","Outubro","Novembro","Dezembro"],
    tickvals=[1,2,3,4,5,6,7,8,9,10,11,12],)
    return line_graph

# Major Product ************************************************************
@app.callback(
    Output(component_id='major-product', component_property='figure'),
    [Input(component_id='product-dd', component_property='value'),
     Input(component_id='country-dd', component_property='value')]
)

def update_plot(input_produto, input_country):
    produto_filter = 'Todos produtos'
    vendasc = vendas.copy(deep=True)
    if input_produto:
        produto_filter = input_produto
        vendasc = vendasc[vendasc['Produto'] == produto_filter]
    if input_country: 
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]    
    vend_bar_major_pdt = vendasc.groupby('Loja')['Faturamento'].agg('sum').reset_index(name='Total')
    bar_graph = px.bar(data_frame=vend_bar_major_pdt,  x='Total',  y = 'Loja', orientation = 'h', title = 'Faturamento total por cidade',
    text_auto=True, color = 'Loja', color_discrete_map={'Sao Paulo':'#abb0ca','Salvador':'#e5cbb0','Rio de Janeiro':'#050507','Porto Alegre':'#e02844',
    'Fortaleza':'#6d6e8c','Curitiba':'#554f64','Brasilia':'#8cac7f'}, labels = dict( Loja = ""))
    bar_graph.update_layout(showlegend=False)
    return bar_graph



# Tree Fig ************************************************************
@app.callback(
    Output(component_id='tree_fig', component_property='figure'),
    [Input(component_id='product-dd', component_property='value'),
     Input(component_id='country-dd', component_property='value')])

def update_plot(input_produto, input_country):    
    vendasc = vendas.copy(deep=True)
    if input_produto:
        produto_filter = input_produto
        vendasc = vendasc[vendasc['Produto'] == produto_filter]  
    if input_country:
        country_filter = input_country
        vendasc = vendasc[vendasc['Loja'] == country_filter]  
   
    vendasg = vendasc.groupby('Loja')['Quantidade Vendida'].agg('sum').reset_index(name='Total')    
    tree_fig = px.treemap(
    data_frame=vendasg, 
    path=['Loja'], 
    values='Total',
    color='Total',   
    title="Unidades vendidas por Cidade",)
    tree_fig.update_coloraxes(showscale=False) 
    tree_fig.update_traces( hovertemplate='Cidade = %{label}<br>Total = %{value}<extra></extra>')    
    return tree_fig


if __name__=='__main__':
    app.run_server(debug=True, process.env.PORT || 3000)