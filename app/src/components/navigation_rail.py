import flet as ft
import asyncio

from contexts import *
from states import AppState

@ft.component
def ToggleRailButton(extended) -> ft.Control:
    theme = ft.use_context(ThemeContext)

    return ft.FloatingActionButton(
        icon=ft.Icon(
            ft.CupertinoIcons.SIDEBAR_LEFT,
            color=theme.colors["bg"],
        ),
        bgcolor=theme.colors["bg_02"],
        margin=0,
        mini=True,
        # expand_losse=True,
        shape=ft.RoundedRectangleBorder(radius=16),
        on_click=lambda _: theme.toggle(),
    )

@ft.component
def AppNavigationRail(app:AppState) -> ft.Control:
    def navigate(e: ft.ControlEvent):
        route = app.pages[e.control.selected_index].route
        if route != app.route:
            asyncio.create_task(ft.context.page.push_route(route))
    
    def toggle_rail(e: ft.ControlEvent):
        set_extended(not extended)

    theme = ft.use_context(ThemeContext)

    extended, set_extended = ft.use_state(False)

    return ft.NavigationRail(
        selected_index=app.get_page_index(),
        on_change=lambda e: navigate(e),
        label_type=ft.NavigationRailLabelType.SELECTED,
        group_alignment=-1.0,
        extended=extended,
        indicator_color=theme.colors["bg"],
        indicator_shape=ft.RoundedRectangleBorder(radius=16),
        leading=ft.FloatingActionButton(
            content=ft.Icon(
                ft.CupertinoIcons.SIDEBAR_LEFT,
                color=theme.colors["text"],
                size=24
            ),
            bgcolor=theme.colors["bg_01"],
            mini=True,
            shape=ft.RoundedRectangleBorder(radius=16),
            margin=8,
            on_click=lambda e: toggle_rail(e),
        ),
        destinations=[
            ft.NavigationRailDestination(
                selected_icon=ft.Icon(
                    icon=page.icon,
                    color=theme.colors["primary"],
                    size=24,
                    expand=True
                ), 
                icon=ft.Icon(
                    icon=page.icon,
                    color=theme.colors["text"],
                    size=24,                    
                    expand=True
                ), 
                label=ft.Text(
                    page.name, 
                    expand=True, 
                    text_align=ft.TextAlign.CENTER,
                    width=80 if extended else None,
                ),
                expand=True,
            ) for page in app.pages
        ],
    )
