## Docucmentation for the `build_graph_div` function 

The function, `build_graph_div` is used to build any graph element in the dashboard. 
  
Params:  
- **`figure`** : `plotly.figure` object or `dash.dcc.Graph` id (`str`).   
This is the figure object to display. If using a `dash.dcc.Graph` id, a dash `callback` function is required to update the plot with changes. If using a `plotly.figure` object, the plot will be static, regardless of user input.    
- **`section_header`** : `str` or `str`-like  
This is the title of the section. It can not be dynamically adjusted.   
- **`**kwargs`**:  
  - **`enable_dropdown`**: `bool`   
        Enables the dropdown functionality. The dropdown functionality will add a `dcc.Dropdown` object to the graph `Div`.  
  - **`dropdown_options`**: `Dict` or `List`  
        The list of dropdown options to display to users. Standard `dcc.Dropdown` object functionality.  
        ***Note**:This only gets checked if* `enable_dropdown` *is* `True`.  
  - **`dropdown_id`**: `Str`    
        The dropdown ID that corresponds to an dash callback function `Input`. This `dropdown_id` is used to update plots depending on input.   
        ***Note**:This only gets checked if* `enable_dropdown` *is* `True`.  
  - **`multi_dropdown`**: `bool`    
        Enables a dropdown menu with multiple selections.  
        ***Note**:This only gets checked if* `enable_dropdown` *is* `True`. 
    
  - **`enable_radio`**: `bool`   
      Enables the radio functionality. The dropdown functionality will add a `dcc.RadioItems` or `dcc.Checklist` object to the graph `Div`.  
  - **`radio_options`**: `Dict` or `List`  
      The list of radio options to display to users. Standard `dcc.RadioItem` or `dcc.Checklist` object functionality.  
      ***Note**:This only gets checked if* `enable_radio` *is* `True`.  
  - **`radio_id`**: `Str`    
      The radio ID that corresponds to an dash callback function `Input`. This `radio_id` is used to update plots depending on input.   
      ***Note**:This only gets checked if* `enable_radio` *is* `True`.  
  - **`multi_radio`**: `bool`    
      Enables a radio menu with multiple selections. In Dash, this is a `dcc.Checklist` object.   
      ***Note**:This only gets checked if* `enable_radio` *is* `True`.   
