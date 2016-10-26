# Georgia Historic Newspapers
#### aka ChronAm for the DLG

## Preparing Batches

In order to import batches, batches must conform to the [NDNP Digital Assets format](http://www.loc.gov/ndnp/guidelines/examples.html) [(examples)](http://chroniclingamerica.loc.gov/data/batches/).

But since we aren't NDNP awardees, we have to hack some things...

### Setting up Database for DLG Batches

1. clear out any existing loaded batches with `dlg\hacks\clear_loaded_batch_data.sql`
2. execute `dlg/hacks/setup_dlg.sql` to setup the DLG as an awardee and institution

### Loading Batches

1. place batch files in `data/dlg_batches`
2. ensure that an xml file containing MARC data for the Titles contained in the batch is present in the `data/nonlccn` directory with the filename `{newspaper_lccn}.xml`
3. run the chronam load_batch job like this:

`core/manage.py load_batch /full_path_to/chronam/data/dlg_batches/properly_named_batch_folder`
