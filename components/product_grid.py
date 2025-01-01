from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

def create_grid(data, page_size=10):
    """
    Membuat tabel AgGrid dengan pagination
    """
    gb = GridOptionsBuilder.from_dataframe(data)
    gb.configure_pagination(paginationAutoPageSize=False, paginationPageSize=page_size)
    gb.configure_default_column(sorteable=True, filterable=True)
    
    grid_options = gb.build()
    
    return AgGrid(
        data,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        allow_unsafe_jscode=True,
        theme='dark'
    )