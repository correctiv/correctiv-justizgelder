# Database for [Spendengerichte](http://spendengerichte.correctiv.org/) story

This is a Django app that can be used in a project. It's also a Django CMS app that can be integrated into a CMS.

## Load the CSV file:

        python manage.py justizgelder_import justizgelder.csv

The CSV loading can take quite some time as the loading code is not optimized (PR welcome).

## Update Index:

If data is updated, it also needs to be re-indexed in order for the search
functionality to work properly:

        python manage.py justizgelder_reindex

