# Known Defects

No live model pickled in this repository. There is only a dataset with locally generated predictions. (Refer to labs-CitySpireB-about.md)

- No filter on input data. Leaving empty fields will freeze the API. 
The problem exists because of a wrong architecture picked. To make a ClientTest for input data, it is necessary to create a separate /GET route. 
