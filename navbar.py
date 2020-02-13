import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

def Navbar():
  # navbar = html.Header([
    # dbc.NavbarSimple(
    #     children=[
    #       dbc.NavItem(dbc.NavLink("Arctic Sea Ice Extent", href="/time-series")),
    #       dbc.DropdownMenu(
    #           nav=True,
    #           in_navbar=True,
    #           label="Menu",
    #           children=[
    #             dbc.DropdownMenuItem("Arctic Sea Ice", href="/ice"),
    #             dbc.DropdownMenuItem("Entry 2"),
    #             dbc.DropdownMenuItem(divider=True),
    #             dbc.DropdownMenuItem("Entry 3"),
    #                   ],
    #               ),
    #             ],
    #   brand="Home",
    #   brand_href="/home",
    #   sticky="top",
    # )
  # ])
  navbar = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Link('Home', href='/'),
    dcc.Link('Arctic Sea Ice', href='/ice'),
    html.Div(id='page-content')
  ])
  return navbar
