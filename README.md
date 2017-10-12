# Georgia Historic Newspapers
#### aka ChronAm for the DLG

[https://gahistoricnewspapers.galileo.usg.edu]

## What's Different?

Building on baseline ChronAm, we added:
1. Calendar support (thanks Nebraska)
2. Browsing by Newspaper Type, Region, City
3. Static Pages for Help, Participation, etc.
4. SolrCloud support

## Loading Batches

1. place batch files in `data/dlg_batches`
2. ensure that an xml file containing MARC data for the Titles contained in the batch is present in the `data/nonlccn` directory
3. run the chronam load_batch job like this:

`manage.py load_batch path_to_batch_folder`

## Preparing Batches

In order to import batches, batches must conform to the [NDNP Digital Assets format](http://www.loc.gov/ndnp/guidelines/examples.html) [(examples)](http://chroniclingamerica.loc.gov/data/batches/).

But since we aren't NDNP awardees, we have to hack some things...

### Setting up Database for DLG Batches

1. clear out any existing loaded batches with `dlg\hacks\clear_loaded_batch_data.sql`
2. execute `dlg/hacks/setup_dlg.sql` to setup the DLG as an awardee and institution

### Apply refinements to the `core_place` table data

GHNP enhances the `core_place` table data to support the included
browsing features. This includes a new model `core_region` that is related to
each place entry that is in Georgia. As well, the county and city values
are extracted from the core-loaded data.

1. `manage.py loaddata regions`
2. `manage.py refine_places`

## Update development Solr config

From Solr dir:

1. Delete old config: `bin/solr zk rm /configs/ghnp/managed-schema -n ghnp -d /opt/chronam/solr/ -z localhost:9983`
2. Load new config: `bin/solr zk upconfig -n ghnp -d /opt/chronam/solr/ -z localhost:9983`
3. Restart Solr

### Disclaimer

This is my first `django` project