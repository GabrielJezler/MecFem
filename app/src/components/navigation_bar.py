import flet as ft
import asyncio

from states import *
from contexts import *

@ft.component
def AppNavigationBar(app:AppState) -> ft.Control:
    def navigate(e: ft.ControlEvent):
        route = app.pages[e.control.selected_index].route
        if route != app.route:
            asyncio.create_task(ft.context.page.push_route(route))

    theme = ft.use_context(ThemeContext)

    return ft.NavigationBar(
        selected_index=app.get_page_index(),
        on_change=lambda e: navigate(e),
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(
                    icon=page.icon,
                    color=theme.colors["text"] if app.get_page_index() != i else theme.colors["bg"]
                ), 
                label=page.name,
            ) for i, page in enumerate(app.pages)
            
        ],
    )