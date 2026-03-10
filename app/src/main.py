import flet as ft
import asyncio

import themes
import pages
from utils import tomltools
from components import AppNavigationRail
from contexts import *
from states import *
from page_data import Page

@ft.component
def MecApp():
    def update_page_config():
        page.title = "MecApp"
        page.theme_mode = app.theme_mode
        page.bgcolor = app.colors["ui"][str(app.theme_mode.value)]["bg"]
        page.padding = 8
        page.theme = ft.Theme(
            text_theme=themes.text.theme(app.theme_mode),
            navigation_rail_theme=themes.navigation_rail.theme(app.theme_mode),
            dropdown_theme=themes.dropdown.theme(app.theme_mode),
            button_theme=themes.button.theme(app.theme_mode),
            text_button_theme=themes.text_button.theme(app.theme_mode),
            tooltip_theme=themes.tooltip.theme(app.theme_mode)
        )

    def navigate(e: ft.ControlEvent):
        route = main_pages[e.control.selected_index].route
        if route != app.route:
            asyncio.create_task(page.push_route(route))

    def get_page_by_route() -> Page:
        routes = [page.route for page in main_pages]
        if app.route in routes:
            return main_pages[routes.index(app.route)]
        else :
            return main_pages[routes.index("/")]
    
    page = ft.context.page

    colors = tomltools.load_colors()
    config = tomltools.load_config()

    simulation_data = SimulationState()

    app, _ = ft.use_state(
        AppState(
            route=page.route,
            theme_mode=ft.ThemeMode.DARK if config["theme"]["mode"] == "dark" else ft.ThemeMode.LIGHT,
            colors=colors,
            config=config,
            simulation_data=simulation_data
        )
    )

    home_page = Page(
        name="Home",
        content=pages.home(app),
        icon=ft.CupertinoIcons.HOME,
        route="/",
        index=0
    )

    material_page = Page(
        name="Material",
        content=pages.material(app),
        icon=ft.CupertinoIcons.LAB_FLASK,
        route="/material",
        index=1
    )

    mesh_page = Page(
        name="Mesh",
        content=pages.mesh(app),
        icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
        route="/mesh",
        index=2
    )

    setup_page = Page(
        name="Setup",
        content=pages.setup(app),
        icon=ft.CupertinoIcons.DOC_CHART,
        route="/setup",
        index=3
    )

    run_page = Page(
        name="Run",
        content=pages.run(app),
        icon=ft.CupertinoIcons.PLAY,
        route="/run",
        index=5
    )

    post_page = Page(
        name="Post",
        content=pages.post(app),
        icon=ft.CupertinoIcons.GRAPH_SQUARE,
        route="/post",
        index=6
    )

    main_pages = [
        home_page, 
        material_page, 
        mesh_page,
        setup_page,
        run_page,
        post_page
    ]
    
    page.on_route_change = app.route_change
    page.on_view_pop = app.view_popped

    toggle = ft.use_callback(lambda: app.toggle_theme(), dependencies=[app.theme_mode])

    theme_value = ft.use_memo(
        lambda: ThemeContextValue(mode=app.theme_mode, toggle=toggle),
        dependencies=[app.theme_mode, toggle],
    )

    ft.on_mounted(update_page_config)
    ft.on_updated(update_page_config, [app.theme_mode])

    return ThemeContext(
        theme_value,
        # lambda: AppContext(
        #     app,
            lambda: ft.Row(
                expand=True,
                spacing=0,
                controls=[
                    AppNavigationRail(
                        app=app,
                        pages=main_pages,
                        selected_index=main_pages.index(get_page_by_route()),
                        on_change=navigate
                    ),
                    ft.VerticalDivider(
                        width=1,
                        color=app.colors["ui"][str(app.theme_mode.value)]["text"]
                    ),
                    ft.Container(
                        content=get_page_by_route().content,
                        expand=True
                    ),
                ],
            )
        # )
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(MecApp))