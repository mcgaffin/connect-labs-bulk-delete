from shiny import reactive
from shinyswatch import theme
from shiny.express import input, render, ui
from posit.connect import Client
import pandas as pd

@reactive.effect(priority=100)
@reactive.event(input.delete_button)
def on_delete():
    print(results_df.cell_selection()["rows"])
    for item in results_df.cell_selection()["rows"]:
        content[item].delete()


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

add_selected = lambda d: {**d, "selected": False}
selectable_content = list(map(add_selected, content))


ui.page_opts(title="Connect Explorer", theme=theme.flatly())
with ui.layout_columns(col_widths=(12)):
    with ui.card():
        "Search"
        ui.input_text("search_term", "", "")
        ui.input_action_button("delete_button", "Delete")
        ui.input_action_button("refresh_button", "Refresh")

    with ui.card():
        "Content"


        @render.data_frame
        def results_df():
            df = pd.DataFrame(content, columns=["selected", "title", "last_deployed_time"])
            return render.DataGrid(
                df,
                selection_mode="rows",
                width="100%",
            )


# @render.text
# def text_out():
#     return f"Search Term: {input.search_term()}"


res = None


@reactive.effect
def _():
    print(input.search_term())
    res = client.content.find(title=input.search_term())
    print(f"Search Result Count: { len(res) }")


# @render.express
# def person():
#     with ui.card(class_="mt-3"):
#         ui.h3(input.name())
#         input.years()


# # Define the server logic
# def server(input: Inputs, output: Outputs, session: Session):

#     @reactive.Effect
#     @reactive.event(input.search_button)
#     def _():
#         search_term = input.search_term()
#         if search_term:
#             try:
#                 items = client.content.find(title=search_term)
#                 print(f"------Found {len(items)} content items")
#                 if items:
#                     output.results_table.set(render_table(items))
#                 else:
#                     output.results_table.set("No results found.")
#             except requests.RequestException as e:
#                 output.results_table.set(f"Error: {str(e)}")

# # def render_table(items):
# #     return ui.table(
# #         ui.table_header("Select", "Item"),
# #         *[ui.table_row(ui.input_checkbox(f"checkbox_{i}"), item.title) for i, item in enumerate(items)]
# #     )

# def render_table(items):
#     return ui.table(
#         ui.table_head(ui.tr(ui.th("Select"), ui.th("Item"))),
#         ui.table_body(
#             *[
#                 ui.tr(
#                     ui.td(ui.input_checkbox(f"checkbox_{i}")),
#                     ui.td(item)
#                 )
#                 for i, item in enumerate(items)
#             ]
#         )
#     )

# # Create the app
# app = App(app_ui, server)

# # Run the app
# if __name__ == "__main__":
#     run_app(app)
