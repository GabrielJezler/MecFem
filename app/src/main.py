import flet as ft
import asyncio
from dataclasses import dataclass
from collections.abc import Callable
from typing import Any

import MecFEM as mf

import themes
import pages
from utils import tomltools

@dataclass(frozen=True)
class ThemeContextValue:
    mode: ft.ThemeMode
    toggle: Callable[[], None]

ThemeContext = ft.create_context(ThemeContextValue(ft.ThemeMode.LIGHT, lambda: None))

@ft.observable
@dataclass
class SimulationData:
    material: Any = None
    mesh_path: str = None
    mesh: mf.mesh.Mesh | None = None
    model: Any = None
    ran: bool = False

    def __repr__(self):
        return f"SimulationContextData(material={self.material}, mesh={self.mesh}, model={self.model}, ran={self.ran})"

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
        print(f"Route changed to {e.route}")
        self.route = e.route

    async def view_popped(self, e: ft.ViewPopEvent):
        print("View popped")
        views = ft.unwrap_component(ft.context.page.views)
        if len(views) > 1:
            await ft.context.page.push_route(views[-2].route)

@ft.component
def SimulataionStatus(app:AppState):
    COLORS = tomltools.load_colors()

    # Force re-render by watching the simulation_data object itself
    _ = ft.use_state(app.simulation_data)

    # Determine colors based on current state
    material_color = COLORS["ui"][app.theme_mode.value]["success"] if app.simulation_data.material else COLORS["ui"][app.theme_mode.value]["alert"]
    mesh_color = COLORS["ui"][app.theme_mode.value]["success"] if app.simulation_data.mesh else COLORS["ui"][app.theme_mode.value]["alert"]
    model_color = COLORS["ui"][app.theme_mode.value]["success"] if app.simulation_data.model else COLORS["ui"][app.theme_mode.value]["alert"]
    ran_color = COLORS["ui"][app.theme_mode.value]["success"] if app.simulation_data.ran else COLORS["ui"][app.theme_mode.value]["alert"]

    return ft.Container(
        padding=6,
        border_radius=12,
        bgcolor=COLORS["ui"][app.theme_mode.value]["primary"],
        content=ft.Column(
            spacing=8,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            controls=[
                ft.Text(
                    "Status",
                    style=themes.text.theme(app.theme_mode).title_small,
                    color=COLORS["ui"][app.theme_mode.value]["bg"],
                ),
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.CupertinoIcons.LAB_FLASK,
                            color=material_color,
                            size=20,
                            tooltip=ft.Tooltip(
                                message=app.simulation_data.material.__repr__() if app.simulation_data.material else "No material defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=COLORS["ui"][app.theme_mode.value]["primary"],
                                    border=ft.Border.all(1, COLORS["ui"][app.theme_mode.value]["text"]),
                                )
                            )
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                            color=mesh_color,
                            size=20,
                            tooltip=ft.Tooltip(
                                message=app.simulation_data.mesh.__repr__() if app.simulation_data.mesh else "No mesh defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=COLORS["ui"][app.theme_mode.value]["primary"],
                                    border=ft.Border.all(1, COLORS["ui"][app.theme_mode.value]["text"]),
                                )
                            )
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                ),
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.CupertinoIcons.DOC_CHART,
                            color=model_color,
                            size=20,
                            tooltip=ft.Tooltip(
                                message=app.simulation_data.model.__repr__() if app.simulation_data.model else "No model defined",
                                decoration=ft.BoxDecoration(
                                    bgcolor=COLORS["ui"][app.theme_mode.value]["primary"],
                                    border=ft.Border.all(1, COLORS["ui"][app.theme_mode.value]["text"]),
                                )
                            )
                        ),
                        ft.Icon(
                            icon=ft.CupertinoIcons.PLAY,
                            color=ran_color,
                            size=20,
                        ),
                    ],
                    spacing=8,
                    alignment=ft.MainAxisAlignment.SPACE_AROUND,
                )
            ]
        )
    )

@ft.component
def ThemeButton():
    theme = ft.use_context(ThemeContext)
    COLORS = tomltools.load_colors()

    return ft.FloatingActionButton(
        icon=ft.Icon(
            ft.CupertinoIcons.SUN_MAX_FILL if theme.mode == ft.ThemeMode.LIGHT else ft.CupertinoIcons.MOON_FILL,
            color=COLORS["ui"][theme.mode.value]["bg"],
        ),
        bgcolor=COLORS["ui"][theme.mode.value]["primary"],
        shape=ft.RoundedRectangleBorder(radius=12),
        on_click=lambda _: theme.toggle(),
    )

@ft.component
def AppNavigationRail(app, pages:list[Page], selected_index: int, on_change:Callable[[int], None]):
    return ft.NavigationRail(
        selected_index=selected_index,
        on_change=lambda e: on_change(e),
        label_type=ft.NavigationRailLabelType.ALL,
        group_alignment=-1.0,
        leading=SimulataionStatus(app=app),
        destinations=[
            ft.NavigationRailDestination(
                selected_icon=ft.Icon(
                    icon=page.icon,
                    color=app.colors["ui"][app.theme_mode.value]["bg"]
                ), 
                icon=ft.Icon(
                    icon=page.icon,
                    color=app.colors["ui"][app.theme_mode.value]["text"]
                ), 
                label=page.name,
                indicator_shape=ft.RoundedRectangleBorder(radius=12)
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
        ),
    )


if __name__ == "__main__":
    ft.run(lambda page: page.render(MecApp))