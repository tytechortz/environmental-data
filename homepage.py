import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

from navbar import Navbar

nav = Navbar()

body = dbc.Container(
    [
       dbc.Row(
           [
               dbc.Col(
                  [
                     html.H2("Arctic Sea Ice"),
                     html.P(
                         """\
                      Arctic Sea Ice extent, data from National Snow Ice Data Center"""
                      ),
                      dbc.Button("View details", color="secondary"),
                   ],
                  md=6,
               ),
              dbc.Col(
                 [
                     html.Img(src='assets/ase.jpg', height=300),
                        ]
                     ),
                ]
            )
       ],
className="mt-4",
)

def Homepage():
    layout = html.Div([
    nav,
    body
    ])
    return layout

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.UNITED])
app.layout = Homepage()
if __name__ == "__main__":
    app.run_server()
