# Database for [Spendengerichte](http://spendengerichte.correctiv.org/) story

This is a Django app that can be used in a project. It's also a Django CMS app that can be integrated into a CMS.

[Download the JSON file](https://apps.correctiv.org/media/justizgelder/data/justizgelder.json) or [the CSV file](https://apps.correctiv.org/media/justizgelder/data/justizgelder.csv) and load it into the database. CSV is much slower to load, but might be useful for other things.

        python manage.py loaddata justizgelder.json

Or load the CSV file:

        python manage.py justizgelder_import justizgelder.csv

The CSV loading can take quite some time as the loading code is not optimized (PR welcome).

Start ElasticSearch in another terminal and run

        python manage.py justizgelder_index
