from shiny import reactive
from shinyswatch import theme
from shiny.express import input, render, ui
from posit.connect import Client
from posit.connect.errors import ClientError
import pandas as pd
import sys


@reactive.effect(priority=100)
@reactive.event(input.delete_button)
def on_delete():
    print(results_df.cell_selection()["rows"])
    try:
        for item in results_df.cell_selection()["rows"]:
            content[item].delete()
            ui.notification_show(
                f"Deleted {content[item]['title']}.", type="message", duration=3
            )
    except ClientError as e:
        ui.notification_show(
            f"Could not delete {content[item]['title']}: {e.error_message}",
            type="error",
            duration=10,
        )


@reactive.effect(priority=1)
@reactive.event(input.refresh_button)
def on_refresh():
    global content
    print("Refresh")
    content = client.content.find()


content = None
with Client(
    api_key="ahF4EwonCpeHVLdByWjtCNmncGvWAc4o", url="http://localhost:3939"
) as client:
    content = client.content.find()

# add_selected = lambda d: {**d, "selected": False}
# selectable_content = list(map(add_selected, content))


ui.page_opts(title="Connect Explorer", theme=theme.flatly())
with ui.layout_columns(col_widths=(12)):
    with ui.card():
        ui.input_text("search_term", "Search", "")
        ui.input_action_button("delete_button", "Delete")
        ui.input_action_button("refresh_button", "Refresh")

    with ui.card():
        "Content"

        @render.data_frame
        def results_df():
            df = pd.DataFrame(
                content, columns=["selected", "title", "last_deployed_time"]
            )
            return render.DataGrid(
                df,
                selection_mode="rows",
                width="100%",
            )


res = None


@reactive.effect
def _():
    print(input.search_term())
    res = client.content.find(title=input.search_term())
    print(f"Search Result Count: { len(res) }")
