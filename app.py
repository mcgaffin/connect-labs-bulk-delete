import json
from shiny import reactive
from shinyswatch import theme
from shiny.express import input, render, ui
from posit.connect import Client
from posit.connect.errors import ClientError
import pandas as pd


@reactive.effect
@reactive.event(input.delete_button)
def on_delete():
    try:
        for item in results_df.cell_selection()["rows"]:
            content()[item].delete()
            ui.notification_show(
                f"Deleted {content()[item]['title']}.", type="message", duration=3
            )
    except ClientError as e:
        ui.notification_show(
            f"Could not delete {content()[item]['title']}: {e.error_message}",
            type="error",
            duration=10,
        )

def is_content_modified():
    with Client(
        api_key="ahF4EwonCpeHVLdByWjtCNmncGvWAc4o", url="http://localhost:3939"
    ) as client:
        find_results = client.content.find()
        return hash(json.dumps(find_results))

@reactive.poll(is_content_modified, 1)
def content():
    with Client(
        api_key="ahF4EwonCpeHVLdByWjtCNmncGvWAc4o", url="http://localhost:3939"
    ) as client:
        find_results = client.content.find()
        if len(input.search_term()) == 0:
            return find_results
        else:
            return list(
                filter(lambda c: input.search_term() in c["title"], find_results)
            )


ui.page_opts(title="Connect Explorer", theme=theme.flatly())
with ui.layout_columns(col_widths=(12)):
    with ui.card(fill=False):
        "Actions"
        ui.input_action_button("delete_button", "Delete", width="100px")

    with ui.card():

        ui.input_text("search_term", "Search", "")
        "Content"
        @render.data_frame
        def results_df():
            df = pd.DataFrame(content(), columns=["title", "last_deployed_time"])
            return render.DataGrid(
                df,
                selection_mode="rows",
                width="100%",
            )
