// Social Harvest is a social media analytics platform.
//     Copyright (C) 2014 Tom Maiaroto, Shift8Creative, LLC (http://www.socialharvest.io)
//
//     This program is free software: you can redistribute it and/or modify
//     it under the terms of the GNU General Public License as published by
//     the Free Software Foundation, either version 3 of the License, or
//     (at your option) any later version.
//
//     This program is distributed in the hope that it will be useful,
//     but WITHOUT ANY WARRANTY; without even the implied warranty of
//     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
//     GNU General Public License for more details.
//
//     You should have received a copy of the GNU General Public License
//     along with this program.  If not, see <http://www.gnu.org/licenses/>.

package config

import (
	"bytes"
	//"github.com/asaskevich/govalidator"
	_ "github.com/SocialHarvestVendors/pq"
	"github.com/SocialHarvestVendors/sqlx"
	// _ "github.com/mathume/monet"
	"log"
	"reflect"
	"strconv"
	"time"
)

type SocialHarvestDB struct {
	Postgres *sqlx.DB
	MonetDB  *sqlx.DB
	Series   []string
	Schema   struct {
		Compact bool `json:"compact"`
	}
	RetentionDays int
	PartitionDays int
}

var database = SocialHarvestDB{}

// Optional settings table/collection holds Social Harvest configurations and configured dashboards for persistence and clustered servers it is more or less a key value store.
// Data is stored as JSON string. The Social Harvest config JSON string should easily map to the SocialHarvestConf struct. Other values could be for JavaScript on the front-end.
type Settings struct {
	Key      string    `json:"key" db:"key" bson:"key"`
	Value    string    `json:"value" db:"value" bson:"value"`
	Modified time.Time `json:"modified" db:"modified" bson:"modified"`
}

// Initializes the database and returns the client, setting it to `database.Postgres` in the current package scope
func NewDatabase(config SocialHarvestConf) *SocialHarvestDB {
	// A database is not required to use Social Harvest
	if config.Database.Type == "" {
		return &database
	}
	var err error

	// Holds some options that will adjust the schema
	database.Schema = config.Schema

	switch config.Database.Type {
	case "postgres", "postgresql":
		// Note that sqlx just wraps database/sql and `database.Postgres` gets a sqlx.DB which is essentially a wrapped sql.DB
		database.Postgres, err = sqlx.Connect("postgres", "host="+config.Database.Host+" port="+strconv.Itoa(config.Database.Port)+" sslmode=disable dbname="+config.Database.Database+" user="+config.Database.User+" password="+config.Database.Password)
		if err != nil {
			log.Println(err)
			return &database
		}
		// TODO: Try MonetDB
		// case "monetdb":
		// 	database.MonetDB, err = sqlx.Connect("monetdb", "host="+config.Database.Host+" port="+strconv.Itoa(config.Database.Port)+" dbname="+config.Database.Database+" user="+config.Database.User+" password="+config.Database.Password)
		// 	if err != nil {
		// 		log.Println(err)
		// 		return &database
		// 	}
	}

	// Data older than the (optional) retention period won't be stored.
	database.RetentionDays = config.Database.RetentionDays
	// Optional partitioning (useful for Postgres which has a PARTITION feature)
	database.PartitionDays = config.Database.PartitionDays

	// Keep a list of series (tables/collections/series - whatever the database calls them, we're going with series because we're really dealing with time with just about all our data)
	// These do relate to structures in lib/config/series.go
	database.Series = []string{"messages", "shared_links", "mentions", "hashtags", "contributor_growth"}

	return &database
}

// Saves a settings key/value (Social Harvest config or dashboard settings, etc. - anything that needs configuration data can optionally store it using this function)
// TODO: Maybe just make this update the JSON file OR save to some sort of localstore so the settings don't go into the database where data is harvested
func (database *SocialHarvestDB) SaveSettings(settingsRow Settings) {
	if len(settingsRow.Key) > 0 {

		var count int
		err := database.Postgres.Get(&count, "SELECT count(*) FROM settings;")
		if err != nil {
			log.Println(err)
			return
		}

		// If it already exists, update
		if count > 0 {
			tx, err := database.Postgres.Beginx()
			if err != nil {
				log.Println(err)
				return
			}
			tx.MustExec("UPDATE settings SET value = $1 WHERE key = $2", settingsRow.Value, settingsRow.Key)
			tx.Commit()

		} else {
			// Otherwise, save new
			tx, err := database.Postgres.Beginx()
			if err != nil {
				log.Println(err)
				return
			}
			tx.NamedExec("INSERT INTO settings (key, value, modified) VALUES (:key, :value, :modified)", settingsRow)
			tx.Commit()
		}
	}
	return
}

// Sets the last harvest time for a given action, value, network set.
// For example: "facebook" "publicPostsByKeyword" "searchKeyword" 1402260944
// We can use the time to pass to future searches, in Facebook's case, an "until" param
// that tells Facebook to not give us anything before the last harvest date...assuming we
// already have it for that particular search query. Multiple params separated by colon.
func (database *SocialHarvestDB) SetLastHarvestTime(territory string, network string, action string, value string, lastTimeHarvested time.Time, lastIdHarvested string, itemsHarvested int) {
	lastHarvestRow := SocialHarvestHarvest{
		Territory:         territory,
		Network:           network,
		Action:            action,
		Value:             value,
		LastTimeHarvested: lastTimeHarvested,
		LastIdHarvested:   lastIdHarvested,
		ItemsHarvested:    itemsHarvested,
		HarvestTime:       time.Now(),
	}

	//log.Println(lastTimeHarvested)
	database.StoreRow(lastHarvestRow)
}

// Gets the last harvest time for a given action, value, and network (NOTE: This doesn't necessarily need to have been set, it could be empty...check with time.IsZero()).
func (database *SocialHarvestDB) GetLastHarvestTime(territory string, network string, action string, value string) time.Time {
	var lastHarvestTime time.Time
	var lastHarvest SocialHarvestHarvest
	if database.Postgres != nil {
		database.Postgres.Get(&lastHarvest, "SELECT * FROM harvest WHERE network = $1 AND action = $2 AND value = $3 AND territory = $4", network, action, value, territory)
	}

	// log.Println(lastHarvest)
	lastHarvestTime = lastHarvest.LastTimeHarvested
	return lastHarvestTime
}

// Gets the last harvest id for a given task, param, and network.
func (database *SocialHarvestDB) GetLastHarvestId(territory string, network string, action string, value string) string {
	lastHarvestId := ""
	var lastHarvest SocialHarvestHarvest
	if database.Postgres != nil {
		database.Postgres.Get(&lastHarvest, "SELECT * FROM harvest WHERE network = $1 AND action = $2 AND value = $3 AND territory = $4", network, action, value, territory)
	}

	lastHarvestId = lastHarvest.LastIdHarvested
	return lastHarvestId
}

// Stores a harvested row of data into the configured database.
func (database *SocialHarvestDB) StoreRow(row interface{}) {
	// A database connection is not required to use Social Harvest (could be logging to file)
	if database.Postgres == nil {
		// log.Println("There appears to be no database connection.")
		return
	}

	// If data is to be expired after a certain point, don't try to save data that is beyond that expiration (the harvester can pull in data from the past - sometimes months in the past)
	if database.RetentionDays > 0 {
		// Only certain series will have a "Time" field, if FieldByName("Time") was ran on the wrong row value, then it would panic and crash the application.
		// TODO: Rethink the use of an interface{} here because I worry about the performance with reflection. Or at least benchmark all this.
		// It would stink to have "StoreMessage" and "StoreSharedLink" etc. So interface{} was convenient... But also a little annoying.
		switch row.(type) {
		case SocialHarvestMessage, SocialHarvestSharedLink, SocialHarvestMention, SocialHarvestHashtag:
			v := reflect.ValueOf(row)
			rowTime := v.FieldByName("Time").Interface().(time.Time).Unix()
			now := time.Now().Unix()
			retentionSeconds := int64(database.RetentionDays * 86400)
			if rowTime <= (now - retentionSeconds) {
				// log.Println("Harvested data falls outside retention period.")
				return
			}
		}
	}

	// The downside to not using upper.io/db or something like it is that INSERT statements incur technical debt.
	// There will be a maintenance burden in keeping the field names up to date...But I think it's manageable.
	// ...and values have to be in the right order, maintaining this in a repeated fashion leads to spelling mistakes, etc. All the reasons I HATE dealing with SQL...But oh well.

	var err error

	// The following will insert the data into the supported databases. Certain series will contain more or less data depending on configuration.
	// Compact storage reduces the number of fields stored on series and assumes the database supports JOINs (or is making some other query) to get the data from the `messages` series.
	// This saves on disk space, but increases query complexity. Full flat storage / expanded schema. This uses more disk space, but the queries should be faster.

	if database.Postgres != nil {
		// Check if valid type to store and determine the proper table/collection based on it
		switch row.(type) {
		case SocialHarvestMessage:
			_, err = database.Postgres.NamedExec("INSERT INTO messages (time, harvest_id, territory, network, message_id, contributor_id, contributor_screen_name, contributor_name, contributor_gender, contributor_type, contributor_longitude, contributor_latitude, contributor_geohash, contributor_lang, contributor_country, contributor_city, contributor_region, contributor_city_pop, contributor_likes, contributor_statuses_count, contributor_listed_count, contributor_followers, contributor_verified, message, is_question, category, sentiment, facebook_shares, twitter_retweet_count, twitter_favorite_count, like_count, google_plus_reshares, google_plus_ones) VALUES (:time, :harvest_id, :territory, :network, :message_id, :contributor_id, :contributor_screen_name, :contributor_name, :contributor_gender, :contributor_type, :contributor_longitude, :contributor_latitude, :contributor_geohash, :contributor_lang, :contributor_country, :contributor_city, :contributor_region, :contributor_city_pop, :contributor_likes, :contributor_statuses_count, :contributor_listed_count, :contributor_followers, :contributor_verified, :message, :is_question, :category, :sentiment, :facebook_shares, :twitter_retweet_count, :twitter_favorite_count, :like_count, :google_plus_reshares, :google_plus_ones);", row)
			if err != nil {
				//log.Println(err)
			} else {
				//log.Println("Successful insert")
			}
		case SocialHarvestSharedLink:
			if database.Schema.Compact {
				_, err = database.Postgres.NamedExec("INSERT INTO shared_links (time, harvest_id, territory, network, message_id, contributor_id, type, preview, source, url, expanded_url, host) VALUES (:time, :harvest_id, :territory, :network, :message_id, :contributor_id, :type, :preview, :source, :url, :expanded_url, :host);", row)
			} else {
				_, err = database.Postgres.NamedExec("INSERT INTO shared_links (time, harvest_id, territory, network, message_id, contributor_id, contributor_screen_name, contributor_name, contributor_gender, contributor_type, contributor_longitude, contributor_latitude, contributor_geohash, contributor_lang, contributor_country, contributor_city, contributor_region, contributor_city_pop, type, preview, source, url, expanded_url, host) VALUES (:time, :harvest_id, :territory, :network, :message_id, :contributor_id, :contributor_screen_name, :contributor_name, :contributor_gender, :contributor_type, :contributor_longitude, :contributor_latitude, :contributor_geohash, :contributor_lang, :contributor_country, :contributor_city, :contributor_region, :contributor_city_pop, :type, :preview, :source, :url, :expanded_url, :host);", row)
			}
			if err != nil {
				//log.Println(err)
			}
		case SocialHarvestMention:
			if database.Schema.Compact {
				_, err = database.Postgres.NamedExec("INSERT INTO mentions (time, harvest_id, territory, network, message_id, contributor_id, mentioned_id, mentioned_screen_name, mentioned_name, mentioned_gender, mentioned_type, mentioned_longitude, mentioned_latitude, mentioned_geohash, mentioned_lang) VALUES (:time, :harvest_id, :territory, :network, :message_id, :contributor_id, :mentioned_id, :mentioned_screen_name, :mentioned_name, :mentioned_gender, :mentioned_type, :mentioned_longitude, :mentioned_latitude, :mentioned_geohash, :mentioned_lang);", row)
			} else {
				_, err = database.Postgres.NamedExec("INSERT INTO mentions (time, harvest_id, territory, network, message_id, contributor_id, contributor_screen_name, contributor_name, contributor_gender, contributor_type, contributor_longitude, contributor_latitude, contributor_geohash, contributor_lang, mentioned_id, mentioned_screen_name, mentioned_name, mentioned_gender, mentioned_type, mentioned_longitude, mentioned_latitude, mentioned_geohash, mentioned_lang) VALUES (:time, :harvest_id, :territory, :network, :message_id, :contributor_id, :contributor_screen_name, :contributor_name, :contributor_gender, :contributor_type, :contributor_longitude, :contributor_latitude, :contributor_geohash, :contributor_lang, :mentioned_id, :mentioned_screen_name, :mentioned_name, :mentioned_gender, :mentioned_type, :mentioned_longitude, :mentioned_latitude, :mentioned_geohash, :mentioned_lang);", row)
			}
			if err != nil {
				//log.Println(err)
			}
		case SocialHarvestHashtag:
			if database.Schema.Compact {
				_, err = database.Postgres.NamedExec("INSERT INTO hashtags (time, harvest_id, territory, network, message_id, tag, keyword, contributor_id) VALUES (:time, :harvest_id, :territory, :network, :message_id, :tag, :keyword, :contributor_id);", row)
			} else {
				_, err = database.Postgres.NamedExec("INSERT INTO hashtags (time, harvest_id, territory, network, message_id, tag, keyword, contributor_id, contributor_screen_name, contributor_name, contributor_gender, contributor_type, contributor_longitude, contributor_latitude, contributor_geohash, contributor_lang, contributor_country, contributor_city, contributor_region, contributor_city_pop) VALUES (:time, :harvest_id, :territory, :network, :message_id, :tag, :keyword, :contributor_id, :contributor_screen_name, :contributor_name, :contributor_gender, :contributor_type, :contributor_longitude, :contributor_latitude, :contributor_geohash, :contributor_lang, :contributor_country, :contributor_city, :contributor_region, :contributor_city_pop);", row)
			}
			if err != nil {
				//log.Println(err)
			}
		case SocialHarvestContributorGrowth:
			_, err = database.Postgres.NamedExec(`INSERT INTO contributor_growth (
			time, harvest_id, territory, network, contributor_id, likes, talking_about, were_here, checkins, views, status_updates, listed, favorites, followers, following, plus_ones, comments) VALUES (:time, :harvest_id, :territory, :network, :contributor_id, :likes, :talking_about, :were_here, :checkins, :views, :status_updates, :listed, :favorites, :followers, :following, :plus_ones, :comments);`, row)
			if err != nil {
				// log.Println(err)
			}
		case SocialHarvestHarvest:
			_, err = database.Postgres.NamedExec("INSERT INTO harvest (territory, network, action, value, last_time_harvested, last_id_harvested, items_harvested, harvest_time) VALUES (:territory, :network, :action, :value, :last_time_harvested, :last_id_harvested, :items_harvested, :harvest_time);", row)
			if err != nil {
				//log.Println(err)
			}
		default:
			// log.Println("trying to store unknown collection")
		}
	}

}

// Creates a partition table in a Postgres database
// NOTE: If this fails to run ahead of time, we have a problem... Though checking on a trigger on every insert carries with it too much overhead.
// So I'm going to look into columnar store databases in hopes to find performance there. FDWs for Postgres perhaps and also MonetDB (which should be SQL compatible).
// Though I imagine partitioning will still be a really nice thing to have in the future. Come back to this...
// TODO: Look at this: https://github.com/keithf4/pg_partman ... probably should just use that.
func (database *SocialHarvestDB) CreatePartitionTable(table string) error {
	var err error

	if database.Postgres != nil && database.PartitionDays > 0 {
		t := time.Now()
		df := t.Format("01022006")

		var buffer bytes.Buffer
		buffer.WriteString("CREATE TABLE IF NOT EXISTS ")
		buffer.WriteString(table)
		buffer.WriteString("_")
		buffer.WriteString(df)
		buffer.WriteString(" (LIKE ")
		buffer.WriteString(table)
		buffer.WriteString(" INCLUDING ALL) INHERITS (")
		buffer.WriteString(table)
		buffer.WriteString(");")

		// Unique (if table is in `database.Series` which is a list of tables with harvest_id fields)
		for _, v := range database.Series {
			if table == v {
				buffer.WriteString(`ALTER TABLE "`)
				buffer.WriteString(table)
				buffer.WriteString("_")
				buffer.WriteString(df)
				buffer.WriteString(`" ADD CONSTRAINT "`)
				buffer.WriteString(table)
				buffer.WriteString("_")
				buffer.WriteString(df)
				buffer.WriteString(`_harvest_id_unique" UNIQUE ("harvest_id") NOT DEFERRABLE INITIALLY IMMEDIATE;`)
			}
		}

		//database.PartitionDays

		// TODO: A few of these to provide enough coverage for harvested data. Unfortunately harvested data can date back a few months...
		// So there might even need to be a catch all table that catches data.
		dfu := t.Format("2006-01-02")
		dfl := t.Format("2006-01-02")
		// TODO
		//const day = 24 * 60 * 60
		//lowerTime := time.Unix((t.Unix() - (database.PartitionDays * day)))
		//dfl := lowerTime.Format("2006-01-02")

		// ...and create/update the trigger when we make the new partiton. This way the trigger is always kept in sync with the partition tables available
		buffer.WriteString(" CREATE OR REPLACE FUNCTION public.")
		buffer.WriteString(table)
		buffer.WriteString("_part_insert_tgr_func() ")
		buffer.WriteString("RETURNS TRIGGER AS $$ ")
		buffer.WriteString("BEGIN ")
		buffer.WriteString("IF( NEW.time >= '")
		// lower time limit
		buffer.WriteString(dfl)
		buffer.WriteString("' AND NEW.time < '")
		// upper time limit
		buffer.WriteString(dfu)
		buffer.WriteString("' ) THEN ")
		buffer.WriteString("INSERT INTO public.")
		buffer.WriteString(table)
		buffer.WriteString("_")
		//buffer.WriteString(df) // date
		buffer.WriteString(" VALUES (NEW.*); ")
		buffer.WriteString("ELSE ")
		buffer.WriteString("RAISE EXCEPTION 'Date out of range. Fix trigger function.'; ")
		buffer.WriteString("END IF; ")
		buffer.WriteString("RETURN NULL; ")
		buffer.WriteString("END; ")
		buffer.WriteString("$$ ")
		buffer.WriteString("LANGUAGE plpgsql; ")

		// Set a trigger to call the function (only needs to be set once... - is there a create trigger if not exists?)
		buffer.WriteString("CREATE TRIGGER partition_insert_trigger BEFORE INSERT ON ")
		buffer.WriteString(table)
		buffer.WriteString(" FOR EACH ROW EXECUTE PROCEDURE public.")
		buffer.WriteString(table)
		buffer.WriteString("_part_insert_tgr_func();")

		// CREATE OR REPLACE FUNCTION my_schema.my_data_insert_trigger_function()
		// RETURNS TRIGGER AS $$
		// BEGIN
		//     IF ( NEW.create_date >= '2010-01-01' AND NEW.create_date < '2010-02-01' ) THEN
		//         INSERT INTO my_schema.my_data_201001 VALUES (NEW.*);
		//     ELSE
		//         RAISE EXCEPTION 'Date out of range.  Fix parent_insert_trigger_function()!';
		//     END IF;
		//     RETURN NULL;
		// END;
		// $$
		// LANGUAGE plpgsql;

		// -- Create a trigger to call the function before insert.
		// CREATE TRIGGER my_data_insert_trigger
		//     BEFORE INSERT ON my_schema.my_data
		//     FOR EACH ROW EXECUTE PROCEDURE my_schema.my_data_insert_trigger_function();

		query := buffer.String()
		buffer.Reset()

		_, err = database.Postgres.Exec(query)
	}
	return err
}

// Checks access to the database
func (database *SocialHarvestDB) HasAccess() bool {
	var err error

	if database.Postgres != nil {
		var c int
		err = database.Postgres.Get(&c, "SELECT COUNT(*) FROM messages")
		if err == nil {
			return true
		} else {
			return false
		}
	}

	return false
}
