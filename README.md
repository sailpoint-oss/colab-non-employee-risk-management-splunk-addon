# NERM Splunk Add-on

The SailPoint NERM Add-on is an open-source splunk add-on built using the Splunk Add-on builder. This add-on helps ingest, parse and normalize data from NERM API into Splunk allowing users to easily search and analyze their data.
It leverages Splunk's data onboarding framework providing a seamless experience for integrating data into Splunk Enterprise and Splunk Cloud.
The SailPoint NERM(Non-Employee Risk Management) API is a RESTful API designed to manage and automate identity governance processes for non-employee identities within SailPoint platform. 
Non-Employee Risk Management (NERM) is an add-on to Identity Security Cloud (ISC) that helps organizations track non-employees such as contractors, partners, and vendors, and their lifecycles within the organization.

For more information about the /search API used by the add-on, see https://developer.sailpoint.com/docs/api/nerm/v1/search/.


## Key Features:
  * Pre-built data inputs for easy ingestion with data source
  * Index each record as an event
  * Field extractions and lookups for enhanced data enrichment


## Compatibility:
* Splunk Enterprise: Version 9.x and above
* Splunk Cloud: Supported(requires app-vetting)
* Add-on builder version: 4.x


## Pre-requisites:

* Splunk Enterprise and Splunk Cloud instance with admin access
* API Access
  		- Tenant Name
  		- API Token [How to generate token](https://documentation.sailpoint.com/ne-admin/help/setup/api.html)


## Authentication:
NERM uses bearer tokens to allow customers to authenticate to NERM API endpoints.
Information on how to generate token is (https://documentation.sailpoint.com/ne-admin/help/setup/api.html)


## Audit Events:
NERM Query for Audit events endpoint provides a search engine for Audit Events by optionally combining subject_type, type, and subject_id to narrow down the audit events.

### Splunk Enterprise/Splunk Cloud:

An event is a single piece of data in Splunk software, similar to a record in a log file or other data input. When data is indexed, it is divided into individual events. Each event is given a timestamp, host, source, and source type. Often, a single event corresponds to a single line in your inputs, but some inputs (for example, XML logs) have multi-line events, and some inputs have multiple events on a single line. When you run a successful search, you get back events. Similar events can be categorized together with event types
//screenshot to be added

### Source Type
Source type is a default field that identifies the data structure of an event. A source type determines how Splunk Enterprise formats the data during the indexing process. Splunk Enterprise comes with a large set of predefined source types, and it assigns a source type to your data. You can override this assignment by assigning an existing source type or creating a custom source type. This add-on creates a custom source type 'sailpoint_nerm_auditevent'. The Splunk indexer identifies and adds the source type field when it indexes the data. As a result, each indexed event has a source type field. A Splunk admin can use the source type field in searches to find all data of a certain type (as opposed to all data from a certain source). The 'sailpoint_nerm_auditevent' source type is straightforward, as seen here:
//screenshot to be added

### Data Input
A Splunk deployment typically has three processing tiers: data input, indexing, and search management. A specific input consumes a raw data stream from its source and annotates each block with some additional metadata (host, source, and source type). Splunk does not look at the contents of the data stream at this point, so the metadata is consistent across all data in a single stream. After raw stream input, the next thing that occurs is the data is parsed into individual events. The ISC add-on creates the events as part of the included scripts. Single data-input exists for the given sourcetype with the ability for the data input to specify execution interval. The ISC add-on defaults the data input interval to 300 seconds (5 minutes).
//screenshot to be added

This input executes a Python script to make HTTP requests to the correct NERM api endpoints, and gather the audit events. In order for this to work, NERM Query for Audit events input much be configured to supply the organization name and API Token Details on the setup and configuration of the data inputs can be found in the 'Setup' section of this document.



## Add-on Packaging

An add-on is type of app that runs on the Splunk platform and provides specific capabilities to other apps, such as getting data in, mapping data, or providing saved searches and macros. An add-on is not typically run as a standalone app. Instead, an add-on is a reusable component that supports other apps across a number of different use cases.
The add-on can be installed directly inside Splunk Enterprise or Splunk cloud.
There are specific requirements and processes you need to follow due to the managed nature of Splunk Cloud. Unlike on-premises Splunk, where you have full control, Splunk Cloud installation require vetting for security, performance and compliance.


* Check Compatibility
  - Ensure the add-on is compatible with Splunk platform.

* Prepare the Add-on package
  - Download the add-on from open-source repository (GitHub)
  - Make the changes and package the add-on.

* Submit the Add-on for App vetting
	- You need to submit the add-on for an App vetting process through Spunk Support or your splunk cloud representative.
  - The vetting process checks for security issues, performance concerns and compliance with Splunk Cloud requriements.
  - To submit, open a support ticket with Splunk support and provide the add-on package(.spl or .tgz file)

* Verify the Add-on Functionality
  - Check the Splunk logs(index=_internal or splunkd.log) for any errors related to the add-on
  - Run test searches to ensure that the add-on is ingesting and parsing events as expected.

* Best Practices:
  - Test in a Development Environment First: Before submitting an add-on for production use, test it in a Splunk development environment or a sandbox instance.
  - Review Security an Compliance: Ensure that the addon does not introduce any security risks(e.g., hard-coded credentials or insecure data handling).
  - Monitor Performance: Keep an eye on resource usage, as changes can affect the Splunk Cloud performance.

* Notes:
  - Some Splunk cloud environment have restricted permissions, in that case you may need to use Splunk Heavy forwarders for data collection and then forward the data to Splunk Cloud or
    you will need to contact Splunk Support for assistance.



## Installation

### Method 1: Install via Splunk Web

* Log in to your splunk instance
* Navigate to **Apps> Manage Apps**
* Click on **Install app from file**
* Upload the .spl file from the release package
* Click **Upload** amd restart Splunk if prompted


### Method 2: Install via Command Line
* Copy the .spl file to your splunk server
* Run the following command
    `splunk install app <add-on-name>.spl`
* Restart the Splunk instance
    'splunk restart`
  

### Method 3: Install on Splunk Cloud
* Navigate to **Splunk Cloud Admin Console > App > Browse More Apps**
* Search for the add-on and click **Install**
* Submit a request to Splunk support to get app cloud certified for installation



## Configuration

### Step 1: Configure Data Inputs

* Go to **Settings > Data Inputs**
* Select the data input
   // Add screenshot
* Click **Add New** and fill in the required details.
   // Add screenshot



## Usage:

##### Basic Search
 `index=<your_index> sourcetype=<sourcetype_name>`

##### Search with Extracted Fields:
 `index=<your_index> sourcetype=<sourcetype_name>`



## Troubleshooting

##### Data not ingesting Properly
   * Verify the data input settings under **Settings > Data Inputs**
   * Check Splunk logs for errors
      'index=_internal sourcetype=splunkd ERROR'

##### Field Extractions Not working
   - Ensure that the source type is correctly assigned
   - Test field extractions using the Field Extractor toll under Settings > Fields

3. Add-on not appearing in App List
   - Confirm the add-on was installed successfully. Check the $SPLUNK_HOME/etc/apps/directory.
   - Ensure the permissions are set correctly(Manage app > Permissions)



## Development and Contribution

This add-on is created using Splunk Add-on builder, which provides a streamlined process for building and testing add-ons with minimal costs. If you want to contribute or modify the add-on:

### Development Setup:

* Clone the repository

* Import the .tgz file in Splunk Add-on Builder.
  // Add the screenshot

* Testing the add-on
  Use the Test feature in add-on builder to validate the changes.



## License:

This add-on is open-sourced and is distributed under the <license-link>



## Support:

For any issues or questions, please reach out via:

GitHub Issues:
Splunk community:








