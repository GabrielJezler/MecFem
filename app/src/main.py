import flet as ft
import asyncio

import themes
import pages
from utils import tomltools
from components import AppNavigationRail, AppNavigationBar, AppBar
from contexts import *
from states import *

@ft.component
def Content(app:AppState):
    theme = ft.use_context(ThemeContext)
    orientation = ft.use_context(OrientationContext)

    ft.context.page.appbar = AppBar(app=app)

    if orientation == ft.Orientation.LANDSCAPE:
        ft.context.page.navigation_bar = None

        return ft.Row(
            expand=True,
            spacing=0,
            controls=[
                AppNavigationRail(
                    app=app,
                ),
                ft.Container(
                    content=app.build_page(),
                    expand=True
                ),
            ],
        )

    elif orientation == ft.Orientation.PORTRAIT:
        ft.context.page.navigation_bar = AppNavigationBar(app=app)

        return ft.Column(
            expand=True,
            spacing=0,
            controls=[
                ft.Container(
                    content=app.build_page(),
                    expand=True
                ),
            ]
        )
    else:
        raise ValueError("Unknown orientation")

@ft.component
def MecApp():
    def update_page_config():
        page.title = "MecApp"
        page.theme_mode = app.theme_mode
        page.bgcolor = theme_value.colors["bg"]
        page.padding = 8
        page.theme = ft.Theme(
            text_theme=themes.text.theme(app.theme_mode),
            navigation_rail_theme=themes.navigation_rail.theme(app.theme_mode),
            dropdown_theme=themes.dropdown.theme(app.theme_mode),
            button_theme=themes.button.theme(app.theme_mode),
            text_button_theme=themes.text_button.theme(app.theme_mode),
            tooltip_theme=themes.tooltip.theme(app.theme_mode),
            navigation_bar_theme=themes.navigation_bar.theme(app.theme_mode),
        )
    
    page = ft.context.page

    config = tomltools.load_config()

    app, _ = ft.use_state(
        AppState(
            route=page.route,
            theme_mode=ft.ThemeMode.DARK if config["theme"]["mode"] == "dark" else ft.ThemeMode.LIGHT,
            config=config,
            pages=[
                PageState(
                    name="Home",
                    content_function=pages.home,
                    icon=ft.CupertinoIcons.HOME,
                    route="/",
                    index=0
                ),
                PageState(
                    name="Material",
                    content_function=pages.material,
                    icon=ft.CupertinoIcons.LAB_FLASK,
                    route="/material",
                    index=1
                ),
                PageState(
                    name="Mesh",
                    content_function=pages.mesh,
                    icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                    route="/mesh",
                    index=2
                ),
                PageState(
                    name="Setup",
                    content_function=pages.setup,
                    icon=ft.CupertinoIcons.DOC_CHART,
                    route="/setup",
                    index=3
                ),
                PageState(
                    name="Run",
                    content_function=pages.run,
                    icon=ft.CupertinoIcons.PLAY,
                    route="/run",
                    index=4
                ),
                PageState(
                    name="Post",
                    content_function=pages.post,
                    icon=ft.CupertinoIcons.GRAPH_SQUARE,
                    route="/post",
                    index=5
                )
            ]
        )
    )

    simulation, _ = ft.use_state(
        SimulationState()
    )

    orientation, set_orientation = ft.use_state(
        page.media.orientation
    )

    def resize(e: ft.ControlEvent):
        print("Resizing, new orientation:", page.media.orientation)
        set_orientation(page.media.orientation)

    def on_keyboard(e: ft.KeyboardEvent):
        if e.shift and e.key == "S":
            page.show_semantics_debugger = not page.show_semantics_debugger

    page.on_route_change = app.route_change
    page.on_view_pop = app.view_popped
    page.on_resize = resize
    page.on_keyboard_event = on_keyboard

    toggle = ft.use_callback(lambda: app.toggle_theme(), dependencies=[app.theme_mode])

    theme_value = ft.use_memo(
        lambda: ThemeContextValue(mode=app.theme_mode, toggle=toggle),
        dependencies=[app.theme_mode, toggle],
    )

    simulation_value = ft.use_memo(
        lambda: SimulationContextValue(state=simulation),
        dependencies=[simulation],
    )

    orientation_value = ft.use_memo(
        lambda: orientation,
        dependencies=[orientation],
    )

    ft.use_effect(update_page_config, [])
    ft.use_effect(update_page_config, [app.theme_mode])

    return OrientationContext(
        orientation_value,
        lambda: ThemeContext(
            theme_value,
            lambda: SimulationContext(
                simulation_value,
                lambda: Content(app)
            )
        )
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(MecApp))