import flet as ft

import themes
import pages
from utils import tomltools
from components import AppNavigationRail, AppNavigationBar, AppBar
from structures.contexts import ThemeContext, SimulationContext, OrientationContext, ThemeContextValue, SimulationContextValue
from structures.states import AppState, PageState, SimulationState

@ft.component
def Content(app:AppState):
    orientation = ft.use_context(OrientationContext)
    colors = ft.use_context(ThemeContext).colors

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
                    bgcolor=colors["bg_01"],
                    border_radius=24,
                    border=ft.Border.all(2, colors["bg_01"]),
                    padding=8,
                    margin=0,
                    content=ft.Column(
                        expand=True,
                        controls=[
                            AppBar(),
                            app.build_page()
                        ],
                        spacing=8,
                    ),
                    expand=True
                ),
            ],
        )
    elif orientation == ft.Orientation.PORTRAIT:
        ft.context.page.navigation_bar = AppNavigationBar(app=app)

        return ft.Container(
            bgcolor=colors["bg_01"],
            border_radius=24,
            border=ft.Border.all(2, colors["bg_01"]),
            padding=8,
            margin=0,
            content=ft.Column(
                expand=True,
                scroll=ft.ScrollMode.AUTO,
                controls=[
                    AppBar(),
                    app.build_page()
                ],
                spacing=8,
            ),
            expand=True
        )
    else:
        raise ValueError("Unknown orientation")

@ft.component
def MecApp():
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
                    content_function=pages.HomeContent,
                    icon=ft.CupertinoIcons.HOME,
                    route="/",
                    index=0
                ),
                PageState(
                    name="Material",
                    content_function=pages.MaterialContent,
                    icon=ft.CupertinoIcons.LAB_FLASK,
                    route="/material",
                    index=1
                ),
                PageState(
                    name="Mesh",
                    content_function=pages.MeshContent,
                    icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                    route="/mesh",
                    index=2
                ),
                PageState(
                    name="Setup",
                    content_function=pages.SetupContent,
                    icon=ft.CupertinoIcons.DOC_CHART,
                    route="/setup",
                    index=3
                ),
                PageState(
                    name="Run",
                    content_function=pages.RunContent,
                    icon=ft.CupertinoIcons.PLAY,
                    route="/run",
                    index=4
                ),
                PageState(
                    name="Post",
                    content_function=pages.PostContent,
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
        if page.media.orientation != orientation:
            set_orientation(page.media.orientation)

    async def on_keyboard(e: ft.KeyboardEvent):
        if e.shift and e.key == "S":
            page.show_semantics_debugger = not page.show_semantics_debugger

        if e.ctrl and e.key.upper() == "T":
            app.toggle_theme()
        
        if e.ctrl and e.key.upper() == "M":
            page.window.maximized = not page.window.maximized
            page.update()
        
        if e.ctrl and e.key.upper() == "W":
            await page.window.close()

        if e.ctrl and e.key == "Tab" and not e.shift:
            current_index = app.get_page_index()
            next_index = (current_index + 1) % len(app.pages)
            await page.push_route(app.pages[next_index].route)
        
        if not e.ctrl and e.key == "Tab" and e.shift:
            current_index = app.get_page_index()
            next_index = (current_index - 1) % len(app.pages)
            await page.push_route(app.pages[next_index].route)

    page.on_route_change = app.route_change
    page.on_view_pop = app.view_popped
    page.on_resize = resize
    page.on_keyboard_event = on_keyboard

    toggle = ft.use_callback(lambda: app.toggle_theme(), dependencies=[app.theme_mode])

    def update_page_config():
        page.title = "MecApp"
        page.theme_mode = app.theme_mode
        page.bgcolor = theme_value.colors["bg"]
        page.padding = 8
        # page.window.title_bar_hidden = True
        page.fonts = {
            "Lora": "fonts/Lora/Lora-VariableFont_wght.ttf",
            "Lora-italic": "fonts/Lora/Lora-Italic-VariableFont_wght.ttf",
            "Nunito": "fonts/Nunito/Nunito-VariableFont_wght.ttf",
            "Nunito-italic": "fonts/Nunito/Nunito-Italic-VariableFont_wght.ttf",
        }
        page.theme = ft.Theme(
            font_family="Nunito",
            text_theme=themes.text.theme(app.theme_mode),
            navigation_rail_theme=themes.navigation_rail.theme(app.theme_mode),
            dropdown_theme=themes.dropdown.theme(app.theme_mode),
            button_theme=themes.button.theme(app.theme_mode),
            text_button_theme=themes.text_button.theme(app.theme_mode),
            tooltip_theme=themes.tooltip.theme(app.theme_mode),
            navigation_bar_theme=themes.navigation_bar.theme(app.theme_mode),
        )
    
    # page.window.icon = "icon.png"

    ft.use_effect(update_page_config, [])
    ft.use_effect(update_page_config, [app.theme_mode])

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