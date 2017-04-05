1. prod-crontab sets 3 cron jobs:
	- daily_update.sh
		- first runs scraper/scraper.py using a date range set in the script
		- for every file it downloaded to /opt/data/raw, it runs parser/parser.py
		- for every file that is xml, it runs solr/ingest.py
		- runs cwod_site/manage.py against three targets:
			- get_date_counts
			- calculate_ngram_tfidf
			- cache_recent_entries
		- finally runs manage.py against apireportfromlogs
	- daily_then_weekly_update.sh
		- just runs cwod_site/manage.py against calculate_ngram_tfidf
	- monthy_update.sh
		- runs cwod_site/manage.py against calculate_ngram_tfidf and calculate_distance.

cwod_site/manage.py targets:
	- cwod.cwod_api.management.commands.get_date_counts
		- calls grep to look up filenames in /opt/data/soldrdocs within the provided date range
		- for each date in those dates:
			- upserts a cwod_api.models.NgramDateCount orm model.
			- upserts an ngrams.models.Date orgm model.
			- prints each date and ngram count
	- cwod.ngrams.management.commands.calculate_ngram_tfidf
		- instantiates a Calculator (local module class).
		- takes a "field" argument that determines which models its going to update in different ways, all of which are defined in cwod.ngrams.models.
	- cwod_site.cwod.management.commands.cache_recent_entries
		- cwod_site/cwod/management/commands/cache_recent_entries.py
		- First sends an orm query for ngrams.models.Date sorted by date in reverse order, then takes the first one. (so, latest timestamp).
		- calls cwod.views.entries_for_date with that date.
			- calls capitolwords.capitolwords.text with that date (this is actually cwod_site.cwod.capitolwords, not the top level file of the same name.)
				- that just hits the capitolwords.org/api endpoint for "text" (NOTE: not sure if this is still reachable).
			- sorts the "entries" then loops through them to do a little dict rearranging
			- keeps the response under 50 chars for some reason
			- finally, sorts some stuff then returns the kv pairs (its returning the .items() result from that dict).
		- sorts the entries returned by entries_for_date
		- for each entry, it creates a new cwod.models.RecentEntry object.
	- apireportfromlogs
		- can't find where this is defined, is it a built in from something?
	- calculate_distance
		- similar to calculate_ngram_tfidf, it uses its own separate version of Calculator to update various Distance* models in cwod.ngrams.models.


- cwod_site.cwod.capitolwords appears to be the main wrapper for a lot of 3rd party api calls.

- capitolwords.org appears to be doa

- data looks like it comes from gpo.gov

- the top level capitolwords.py is the main entry point for the scraper.

daily data pipeline:
	1. Scraper
	2. Parser
	3. ingest.py (solr ingestion)


scraper
	- entry point is retrieve_by_date:
		- sets its date instance variable to the param
		- checks local dirs to see if we've already retrieved zip files for this date.
		- calls was_in_session




- CRParser is intialized.
	- removes this thing: \n\n\n\n\n[[Page D162]]\n\n\n\n\n from the text.
	- also removes *<bullet> *, then sets a flag to say if it found any (self.is_bullet)
	- calls instance method "get_metadata":
		- tries to read in the mods.xml file, if it can't find it, it calls self.download_mods_file.
		- extracts a few fields from the mods file:
			- volume
			- issue
			- congress
			- session
		- also extracts members (reps + sens)
		- + speaker
		- other docs it references
- For each file, parser.parse() is called, which just calls markup_preamble
- that calls markup_chamber
- which then calls markup_pages
- which then calls markup_title
- ... markup_paragraph



item
	extension
		accessId

item['extention']['accessId'] filename component (CREC-2017blahblah)
item['extention']['chamber'] congress/senate
item['extention']['granuleDate'] same date in the filename
item['name'] list of authors (individuals and/or committees)


https://www.gpo.gov/help/index.html#about_congressional_record.htm