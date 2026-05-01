import flet as ft

from structures.contexts import ThemeContext

@ft.component
def Panel(
    title_content:ft.Control,
    expand_content:ft.Control,
    selected:bool=False,
    expand_panel:bool=False,
) -> ft.Control:
    theme = ft.use_context(ThemeContext)

    expand_panel_state, set_expand_panel_state = ft.use_state(expand_panel)

    # def toggle_panel(e: ft.ControlEvent) -> None:

    return ft.Container(
        bgcolor=theme.colors["bg_01"],
        border_radius=16,
        border=ft.Border.all(2, theme.colors["bg_01"]),
        padding=4,
        content=ft.Column(
            spacing=4,
            controls=[
                ft.Row(
                    controls=[
                        ft.Checkbox(
                            value=selected,
                            check_color=theme.colors["primary"],
                            fill_color={
                                ft.ControlState.DEFAULT: theme.colors["bg"],
                                ft.ControlState.SELECTED: theme.colors["primary"],
                            },
                            shape=ft.CircleBorder(),
                            border_side=ft.BorderSide(1, theme.colors["bg_01"]),
                            splash_radius=12.5,
                            expand=1,
                        ),
                        ft.Container(
                            content=title_content,
                            expand=8,
                            on_click=lambda e: set_expand_panel_state(not expand_panel_state),
                        ),
                        ft.IconButton(
                            icon = ft.Icon(
                                ft.CupertinoIcons.CHEVRON_RIGHT if not expand_panel_state else ft.CupertinoIcons.CHEVRON_DOWN,
                                size=16,
                                color=theme.colors["text"],
                            ),
                            expand=1,
                            on_click=lambda e: set_expand_panel_state(not expand_panel_state),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Container(
                    content=expand_content,
                    visible=expand_panel_state,
                )
            ]
        ),
   )