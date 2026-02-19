import flet as ft
import asyncio
from dataclasses import dataclass
from collections.abc import Callable
from typing import Any

import MecFEM as mf

import themes
import components
from utils import tomltools

@dataclass(frozen=True)
class ThemeContextValue:
    mode: ft.ThemeMode
    toggle: Callable[[], None]

ThemeContext = ft.create_context(ThemeContextValue(ft.ThemeMode.LIGHT, lambda: None))

@dataclass
class SimulationData:
    material: Any = None
    mesh_path: str = None
    mesh: mf.mesh.mesh_struct.Mesh | None = None
    model: Any = None

    def __repr__(self):
        return f"SimulationContextData(material={self.material}, mesh={self.mesh}, model={self.model})"

@ft.observable
@dataclass
class Page:
    name: str
    route: str
    index:int
    icon: ft.Icon
    content: ft.Control

@ft.observable
@dataclass
class AppState:
    route: str
    theme_mode: ft.ThemeMode
    colors: dict
    config: dict
    simulation_data: SimulationData

    def toggle_theme(self):
        self.theme_mode = (
            ft.ThemeMode.DARK
            if self.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        
        self.config["theme"]["mode"] = "dark" if self.theme_mode == ft.ThemeMode.DARK else "light"
        tomltools.update_config(self.config)

    def route_change(self, e: ft.RouteChangeEvent):
        self.route = e.route

    async def view_popped(self, e: ft.ViewPopEvent):
        print("View popped")
        views = ft.unwrap_component(ft.context.page.views)
        if len(views) > 1:
            await ft.context.page.push_route(views[-2].route)

@ft.component
def ThemeButton():
    theme = ft.use_context(ThemeContext)
    COLORS = tomltools.load_colors()

    return ft.FloatingActionButton(
        icon=ft.Icon(
            ft.CupertinoIcons.SUN_MAX_FILL if theme.mode == ft.ThemeMode.LIGHT else ft.CupertinoIcons.MOON_FILL,
            color=COLORS["ui"][theme.mode.value]["text"],
        ),
        bgcolor=COLORS["ui"][theme.mode.value]["primary"],
        on_click=lambda _: theme.toggle(),
    )

@ft.component
def AppNavigationRail(pages:list[Page], selected_index: int, on_change:Callable[[int], None]):
    return ft.NavigationRail(
        selected_index=selected_index,
        on_change=lambda e: on_change(e),
        label_type=ft.NavigationRailLabelType.ALL,
        destinations=[
            ft.NavigationRailDestination(
                icon=page.icon, 
                selected_icon=page.icon, 
                label=page.name
            ) for page in pages
        ],
        trailing=ThemeButton(),
    )

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

    simulation_data = SimulationData()

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
        content=components.home(app),
        icon=ft.CupertinoIcons.HOME,
        route="/",
        index=0
    )

    material_page = Page(
        name="Material",
        content=components.material(app),
        icon=ft.CupertinoIcons.LAB_FLASK,
        route="/material",
        index=1
    )

    mesh_page = Page(
        name="Mesh",
        content=components.mesh(app),
        icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
        route="/mesh",
        index=2
    )

    model_page = Page(
        name="Model",
        content=components.model(app),
        icon=ft.CupertinoIcons.DOC_CHART,
        route="/model",
        index=3
    )

    bc_page = Page(
        name="Boundary\nConditions",
        content=components.bc(app),
        icon=ft.CupertinoIcons.ARROW_UP_RIGHT_SQUARE,
        route="/bc",
        index=4
    )

    run_page = Page(
        name="Run",
        content=components.run(app),
        icon=ft.CupertinoIcons.PLAY,
        route="/run",
        index=5
    )

    post_page = Page(
        name="Post",
        content=components.post(app),
        icon=ft.CupertinoIcons.GRAPH_SQUARE,
        route="/post",
        index=6
    )

    main_pages = [
        home_page, 
        material_page, 
        mesh_page,
        model_page,
        bc_page,
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
        lambda: ft.Row(
            expand=True,
            spacing=0,
            controls=[
                AppNavigationRail(
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
        ),
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(MecApp))