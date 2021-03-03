# Modeling

The Prophet model from  the FBProphet library was used to generate the predictions. The FBProphet library is not Pip friendly which means you can't use it unless you have the packages installed some other way. One option you can do is to Conda install the packages. If you are able to have the proper packages installed within this repository; the pickled rent_model.pkl should be usable.

[FBProphet Library Instructions](https://facebook.github.io/prophet/docs/installation.html)

# Deploying
When dealing with FastAPI, make sure you create 1 GET and 1 POST route. The app can function with just with 1 POST route only (in our case), however, in this case you will not be able to test the input data. Having two routes will allow you to create test files and test functions for the input data.

Another tip is deletion of Dockerfile if EB deployment fails. If you see 'Upgrade request error' in your browser, delete dockerfile and replace it with a procfile, stating the version of python there. It's better not to use the newest version of python since some of the dependencies might not be compatible with it yet. 
