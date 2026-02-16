import flet as ft

import themes
import pages
from utils import tomltools

def main(page: ft.Page):
    COLORS = tomltools.load_colors()
    CONFIG = tomltools.load_config()

    page.title = "MecApp"
    page.theme_mode = ft.ThemeMode.DARK if CONFIG["theme"]["mode"] == "dark" else ft.ThemeMode.LIGHT
    page.bgcolor = COLORS["ui"][str(page.theme_mode.value)]["bg"]
    page.padding = 8

    page.theme = ft.Theme(
        text_theme=themes.text.theme(page),
        navigation_rail_theme=themes.navigation_rail.theme(page),
        dropdown_theme=themes.dropdown.theme(page),     
    )

    HOME = pages.home(
        page=page,
        title="Home",
        description="Welcome to the home page of the application.",
    )

    MATERIAL =pages.material(
        page=page,
        title="Material",
        description="Manage materials for your model.",
    )
    
    MESH = pages.mesh(
        page=page,
        title="Mesh",
        description="Create and manage meshes for your model.",
    )

    MODEL = pages.model(
        page=page,
        title="Model",
        description="Create and manage your model.",
    )
    
    BC = pages.bc(
        page=page,
        title="Boundary Conditions",
        description="Define boundary conditions for your model.",
    )

    RUN = pages.run(
        page=page,
        title="Run",
        description="Run the simulation and monitor progress.",
    )

    POST = pages.post(
        page=page,
        title="Post-Processing",
        description="Visualize and analyze simulation results.",
    )

    def routing(e: ft.ControlEvent):
        index = e.control.selected_index
        if index == 0:
            content.content = HOME
        elif index == 1:
            content.content = MATERIAL
        elif index == 2:
            content.content = MESH
        elif index == 3:
            content.content = MODEL
        elif index == 4:
            content.content = BC
        elif index == 5:
            content.content = RUN
        elif index == 6:
            content.content = POST

        page.update()

    def toggle_theme(page: ft.Page):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            CONFIG["theme"]["mode"] = "dark"
        else:
            CONFIG["theme"]["mode"] = "light"

        tomltools.update_config(CONFIG)

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "Theme changed",
                style=themes.text.title_medium(page, color=COLORS["ui"][page.theme_mode.value]["primary"], bold=True)
            ),
            content=ft.Text(
                "Please close and reopen the app to see the changes.",
                style=themes.text.body_medium(page)    
            ),
            actions=[
                ft.TextButton(
                    content=ft.Text("Dismiss", style=themes.text.body_medium(page, color=COLORS["ui"][page.theme_mode.value]["primary"], bold=True)),

                    on_click=lambda _: page.pop_dialog()
                )
            ],
            open=True,
        )

        page.show_dialog(dialog)
        page.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=120,
        min_extended_width=120,
        on_change=routing,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icon(
                    ft.Icons.HOME_OUTLINED,
                    color=COLORS["ui"][page.theme_mode.value]["text"],
                ),
                selected_icon=ft.Icon(
                    ft.Icons.HOME_OUTLINED,
                    color=COLORS["ui"][page.theme_mode.value]["bg"],
                ),
                label="Home",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(
                    ft.CupertinoIcons.LAB_FLASK,
                    color=COLORS["ui"][page.theme_mode.value]["text"],
                ),
                selected_icon=ft.Icon(
                    ft.CupertinoIcons.LAB_FLASK,
                    color=COLORS["ui"][page.theme_mode.value]["bg"],
                ),
                label="Material",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(
                    ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                    color=COLORS["ui"][page.theme_mode.value]["text"],
                ),
                selected_icon=ft.Icon(
                    ft.CupertinoIcons.SQUARE_GRID_4X3_FILL,
                    color=COLORS["ui"][page.theme_mode.value]["bg"],
                ),
                label="Mesh",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(
                    ft.CupertinoIcons.DOC_CHART,
                    color=COLORS["ui"][page.theme_mode.value]["text"],
                ),
                selected_icon=ft.Icon(
                    ft.CupertinoIcons.DOC_CHART,
                    color=COLORS["ui"][page.theme_mode.value]["bg"],
                ),
                label="Model",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(
                    ft.CupertinoIcons.ARROW_UP_RIGHT_SQUARE,
                    color=COLORS["ui"][page.theme_mode.value]["text"],
                ),
                selected_icon=ft.Icon(
                    ft.CupertinoIcons.ARROW_UP_RIGHT_SQUARE,
                    color=COLORS["ui"][page.theme_mode.value]["bg"],
                ),
                label="Boundary\nConditions",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(
                    ft.CupertinoIcons.PLAY,
                    color=COLORS["ui"][page.theme_mode.value]["text"],
                ),
                selected_icon=ft.Icon(
                    ft.CupertinoIcons.PLAY,
                    color=COLORS["ui"][page.theme_mode.value]["bg"],
                ),
                label="Run",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icon(
                    ft.CupertinoIcons.GRAPH_SQUARE,
                    color=COLORS["ui"][page.theme_mode.value]["text"],
                ),
                selected_icon=ft.Icon(
                    ft.CupertinoIcons.GRAPH_SQUARE,
                    color=COLORS["ui"][page.theme_mode.value]["bg"],
                ),
                label="Post",
            ),
        ],
        trailing=ft.FloatingActionButton(
            icon=ft.Icon(
                ft.Icons.BRIGHTNESS_6_OUTLINED,
                color=COLORS["ui"][page.theme_mode.value]["text"],
            ),
            bgcolor=COLORS["ui"][page.theme_mode.value]["primary"],
            on_click=lambda _: toggle_theme(page),
        )
    )

    content = pages.home(
        page=page,
        title="Home",
        description="Welcome to the home page of the application.",
    )

    page.add(
        ft.Row(
            expand=True,
            controls=[
                ft.SelectionArea(content=rail),
                ft.VerticalDivider(width=1, color=COLORS["ui"][page.theme_mode.value]["text"]),
                content
            ],
            spacing=0,
        )
    )


if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
