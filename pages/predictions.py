# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_daq as daq
import pandas as pd
from datetime import date
from tensorflow import keras
import numpy as np
import pickle
import sklearn

# Imports from this application
from app import app
from pred_lists import zip_code, neighborhood, amenities, property, bathrooms_marks
from airbnb_model import *
from model_tools_class import mt


# load model trained on airbnb data
model = keras.models.load_model('airbnb_model')
oe = mt.get_oe()
print('Model loaded successfully')


model_columns = ['property_type',
 'room_type',
 'bed_type',
 'cancellation_policy',
 'city',
 'host_identity_verified',
 'instant_bookable',
 'neighbourhood',
 'zipcode',
 'amenities',
 'accommodates',
 'bathrooms',
 'bedrooms',
 'beds',
 'host_since_days']


# create input form for User
row1 = html.Div(
    [
        # 1st Row. Introductory Marks
        dbc.Row(dbc.Col(html.Div('''Welcome to our predictions page! Fill out the form as accurately as possible,
                                 and we will compare similar properties (bases on amenities and location) and 
                                 provide you with the best estimate for your daily rental price on AirBnB.''', className='mb-4'))),
        # 2nd Row. Includes Property Type, Room Type
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Property Type", className='mb-1'),
                        dcc.Dropdown(
                            id='property',
                            options=property.property_type,
                            className='mb-4',
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Room Type", className='mb-1'),
                        dcc.Dropdown(
                            id='room',
                            options=[
                                {'label': 'Entire Home/Apartment', 'value': 'Entire home/apt'},
                                {'label': 'Private Room', 'value': 'Private room'},
                                {'label': 'Shared room', 'value': 'Shared room'}
                            ],
                            # value='Entire home/apt',
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
        # 3rd Row. Includes Accomadates, number of bathrooms
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Accomadates", className='mb-1'),
                        daq.NumericInput(
                            id='accomadates',
                            min=1,
                            max=16,
                            value=1,
                            className='mb-4',
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Number of Bathrooms", className='mb-1'),
                        dcc.Slider(
                            id='bathrooms',
                            min=0,
                            max=8,
                            step=0.5,
                            marks=bathrooms_marks.bathroom_marks,
                            value=1,
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
        # 4th Row. Includes Bedrooms, Beds
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Number of Bedrooms", className='mb-1'),
                        daq.NumericInput(
                            id='bedrooms',
                            min=0,
                            max=10,
                            value=1,
                            className='mb-4',
                        ),  
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Number of Beds", className='mb-1'),
                        daq.NumericInput(
                            id='beds',
                            min=0,
                            max=18,
                            value=1,
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
        # 5th Row. Includes bed_type, cancellation_policy
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Bed Type", className='mb-1'),
                        dcc.Dropdown(
                            id='bedtype',
                            options=[
                                {'label': 'Real Bed', 'value': 'Real Bed'},
                                {'label': 'Futon', 'value': 'Futon'},
                                {'label': 'Pull-out Sofa', 'value': 'Pull-out Sofa'},
                                {'label': 'Airbed', 'value': 'Airbed'},
                                {'label': 'Couch', 'value': 'Couch'},
                            ],
                            className='mb-4',
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Cancellation Policy", className='mb-1'),
                        dcc.Dropdown(
                            id='cancellation',
                            options=[
                                {'label': 'Strict', 'value': 'strict'},
                                {'label': 'Flexible', 'value': 'flexible'},
                                {'label': 'Moderate', 'value': 'moderate'},
                                {'label': 'Super Strict 30', 'value': 'super_strict_30'},
                                {'label': 'Super Strict 60', 'value': 'super_strict_60'},
                            ],
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
        # 6th Row. Includes cleaning_fee, city
        dbc.Row(
            [
                # dbc.Col(
                #     [
                #         dcc.Markdown("##### Includes Cleaning Fee", className='mb-1'),
                #         daq.BooleanSwitch(
                #             id='cleaning',
                #             on=True,
                #             label='Blue = True',
                #             className='mb-4',
                #         ),
                #     ],
                # ),
                dbc.Col(
                    [
                        dcc.Markdown("##### City", className='mb-1'),
                        dcc.Dropdown(
                            id='city',
                            options=[
                                {'label': 'New York City', 'value': 'NYC'},
                                {'label': 'Los Angeles', 'value': 'LA'},
                                {'label': 'San Francisco', 'value': 'SF'},
                                {'label': 'Washington DC', 'value': 'DC'},
                                {'label': 'Boston', 'value': 'Boston'},
                                {'label': 'Chicago', 'value': 'Chicago'},
                            ],
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
        # 7th Row. Includes host_identity_verified, instant_bookable, host_since_days
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### You Are a Verified Host", className='mb-1'),
                        daq.BooleanSwitch(
                            id='verified_host',
                            on=True,
                            label='Blue = True',
                            className='mb-4',
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Is Instantly Bookable", className='mb-1'),
                        daq.BooleanSwitch(
                            id='bookable',
                            on=True,
                            label='Blue = True',
                            className='mb-4',
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Host Start Date", className='mb-1'),
                        dcc.DatePickerSingle(
                            id='days_host',
                            date=date(2010, 1, 1)
                        )
                    ],
                ),
            ]
        ),
        # 8th Row. Includes neighbourhood, zipcode
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Neighborhood", className='mb-1'),
                        dcc.Dropdown(
                            id='neighborhood',
                            options=neighborhood.neighborhoods,
                            className='mb-4',
                        ),
                    ],
                ),
                dbc.Col(
                    [
                        dcc.Markdown("##### Zipcode", className='mb-1'),
                        dcc.Dropdown(
                            id='zipcode',
                            options=zip_code.total_zip,
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
        # 9th Row. Includes amenities
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Markdown("##### Amenities", className='mb-1'),
                        # dcc.Checklist(
                        #     id='amenities',
                        #     options=amenities.amenity,
                        #     inputStyle={"margin-right": '8px'},
                        #     labelStyle = {'margin-right':'15px'}
                        # )
                        dcc.Slider(
                            id='amenities',
                            min=0,
                            max=39,
                            step=1,
                            value=1,
                            className='mb-4',
                        ),
                    ],
                ),
            ]
        ),
    ]
)


# output section that returns estimated price based off inputs
row2 = html.Div(
    dbc.Col(
        [
            html.H2('Price Estimation', className='mb-5'), 
            # html.Div(id='prediction-content', className='lead')
        ]
    )
)



button = html.Div(
                [
                    dbc.Button("Predict Price", id="example-button", className="mr-2"),
                    html.Div(id='container-button-timestamp'),
                    html.Span(id="example-output", style={"vertical-align": "middle"}),
                ]
            )

@app.callback(
    Output("container-button-timestamp", "children"), [Input("example-button", 'n_clicks')], 
        [State('property', component_property='value'), State('room', component_property='value'),
        State('accomadates', component_property='value'), State('bathrooms', component_property='value'),
        State('bedrooms', component_property='value'), State('beds', component_property='value'),
        State('bedtype', component_property='value'), State('cancellation', component_property='value'),
        State('city', component_property='value'), State('verified_host', component_property='value'),
        State('bookable', component_property='value'), State('days_host', component_property='value'),
        State('neighborhood', component_property='value'), State('zipcode', component_property='value'),
        State('amenities', component_property='value')]
)
def on_button_click(n, property, room, accomadates, bathrooms, bedrooms, beds, bedtype, cancellation, city, verified_host, bookable, days_host, neighborhood, zipcode, amenities):
    if n is None:
        return "Not clicked."
    else:
        # return bathrooms
        return predict(property, room, accomadates, bathrooms, bedrooms, beds, bedtype, cancellation, city, verified_host, bookable, days_host, neighborhood, zipcode, amenities)[0]


# callback function for output
# @app.callback(
#     Output('prediction-content', 'children'),
#     [
#         Input('property', 'value'), Input('room', 'value'), Input('accomadates', 'value'),
#         Input('bathrooms_1', 'value'), Input('bedrooms', 'value'), Input('beds', 'value'),
#         Input('bedtype', 'value'), Input('cancellation', 'value'),Input('city', 'value'), 
#         Input('verified_host', 'value'), Input('bookable', 'value'), Input('days_host', 'value'),
#         Input('neighborhood', 'value'), Input('zipcode', 'value'), Input('amenities', 'value')
#     ],
# )
def predict(
    property, room, accomadates, bathrooms,
    bedrooms, beds, bedtype, cancellation,
    city, verified_host, bookable,
    days_host, neighborhood, zipcode, amenities
    ):
    df = pd.DataFrame(
        columns=[
            'property_type', 'room_type', 'accommodates', 'bathrooms',
            'bedrooms', 'beds', 'bed_type', 'cancellation_policy',
            'city', 'host_identity_verified', 'instant_bookable',
            'host_since_days', 'neighbourhood', 'zipcode', 'amenities'
        ], 
        data=[
                [
                property, room, accomadates, bathrooms,
                bedrooms, beds, bedtype, cancellation,
                city, verified_host, bookable,
                days_host, neighborhood, zipcode, amenities
                ]
        ]
    )
    # y_pred, confirm_df = get_prediction(df)
    return get_prediction(df)
    # return f'{y_pred:.0f} dollars per day'
def get_prediction(df):
    df=pd.DataFrame(
        data=[
            [
                'Apartment',
                'Entire home/apt',
                'Real Bed',
                'strict',
                'NYC',
                'True',
                'False',
                'Brooklyn Heights',
                '11201',
                8,
                3,
                1.0,
                1.0,
                1.0,
                4074
            ]
        ], 
        columns=[
            'property_type',
            'room_type',
            'bed_type',
            'cancellation_policy',
            'city',
            'host_identity_verified',
            'instant_bookable',
            'neighbourhood',
            'zipcode',
            'amenities',
            'accommodates',
            'bathrooms',
            'bedrooms',
            'beds',
            'host_since_days'
        ]
            
    )
    string_variable_list = ['property_type','room_type','bed_type',
                            'cancellation_policy','city','host_identity_verified',
                            'instant_bookable','neighbourhood','zipcode']
    number_variable_list = ['amenities','accommodates','bathrooms','beds','bedrooms','host_since_days']
    number_value_list = []
    string_value_list = []
    for x in string_variable_list:
        string_value_list.append(df[x])
    for x in number_variable_list:
        if type(df[x]) != str and type(df[x]) != np.int64 and type(df[x]) != np.float64 and type(df[x]) != np.bool:
            number_value_list.append(mt.get_days(df[x]))
        else:
            number_value_list.append(df[x])

    string_vectorized= oe.transform(np.array(string_value_list).reshape(1,-1))
    whole_input_vector = string_vectorized[0].tolist() + number_value_list
    confirm_df = get_confirm_df(string_vectorized,number_value_list,string_value_list)

    prediction = model.predict(np.array(whole_input_vector).reshape(1,-1))
    return prediction[0][0], confirm_df


def get_confirm_df(input_list_objects,input_list_numbers,string_value_list):
    df_rows = []
    for i in np.arange(9):
        df_rows.append((model_columns[i],string_value_list[i],input_list_objects[0][i]))
    for i in np.arange(9,len(model_columns)):
        df_rows.append((model_columns[i],input_list_numbers[i-9],input_list_numbers[i-9]))
    confirm_df = pd.DataFrame(df_rows,columns=['Variable','Value','Encoded'])
    return confirm_df




# layout of the page
layout = dbc.Row([row1, row2, button])





