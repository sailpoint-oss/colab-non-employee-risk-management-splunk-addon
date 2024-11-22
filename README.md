# Non-employee Risk Management Splunk Add-on

The SailPoint Non-employee Risk Management AuditEvent Add-on is an open-source splunk add-on built using the Splunk Add-on builder. This add-on helps ingest, parse and normalize data from Non-employee Risk Management(NERM) API into Splunk allowing users to easily search and analyze their data.
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
Non-employee Risk Management(NERM) uses bearer tokens to allow customers to authenticate to Non-employee Risk Management() API endpoints.
Information on how to generate token is (https://documentation.sailpoint.com/ne-admin/help/setup/api.html)


## Audit Events:
Non-employee Risk Management(NERM) Query for Audit events endpoint provides a search engine for Audit Events by **optionally** combining subject_type, type, and subject_id to narrow down the audit events.


### Splunk Enterprise/Splunk Cloud:

An event is a single piece of data in Splunk software, similar to a record in a log file or other data input. When data is indexed, it is divided into individual events. Each event is given a timestamp, host, source, and source type. Often, a single event corresponds to a single line in your inputs, but some inputs (for example, XML logs) have multi-line events, and some inputs have multiple events on a single line. When you run a successful search, you get back events. Similar events can be categorized together with event types.


### Source Type
Source type is a default field that identifies the data structure of an event. A source type determines how Splunk Enterprise formats the data during the indexing process. Splunk Enterprise comes with a large set of predefined source types, and it assigns a source type to your data. You can override this assignment by assigning an existing source type or creating a custom source type. This add-on creates a custom source type 'sailpoint_non-employee_risk_management'. The Splunk indexer identifies and adds the source type field when it indexes the data. As a result, each indexed event has a source type field. A Splunk admin can use the source type field in searches to find all data of a certain type (as opposed to all data from a certain source). 


### Data Input
A Splunk deployment typically has three processing tiers: data input, indexing, and search management. A specific input consumes a raw data stream from its source and annotates each block with some additional metadata (host, source, and source type). Splunk does not look at the contents of the data stream at this point, so the metadata is consistent across all data in a single stream. After raw stream input, the next thing that occurs is the data is parsed into individual events. This add-on creates the events as part of the included scripts. Single data-input exists for the given sourcetype with the ability for the data input to specify execution interval. Recommended data input interval is 300 seconds (5 minutes).

<img width="800" alt="Screenshot 2024-11-15 at 12 10 29 PM" src="https://github.com/user-attachments/assets/f49cd169-376d-4ce3-af63-40acf96114e5">



This input executes a Python script to make HTTP requests to the correct Non-employee Risk Management(NERM) api endpoints, and gather the audit events. In order for this to work, Non-employee Risk Management(NERM) Query for Audit events input much be configured to supply the Tenant Name, Tenant URL and API Key on the setup and configuration page of the add-on.



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
  - You need to submit the add-on for an App vetting process through Spunk Support or your Splunk cloud representative.
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
* Upload the .tar.gz file from **/build** directory
* Click **Upload** and restart Splunk if prompted
* Find **SailPoint Non-employee Risk Management AuditEvent Add-on** from the list and click **Launch App**
  

### Method 2: Install on Splunk Cloud
* Navigate to **Splunk Cloud Admin Console > App > Browse More Apps**
* Search for the add-on and click **Install**
* Submit a request to Splunk support to get app cloud certified for installation



## Configuration

### Step 1: Configure Data Inputs

* Navigate to **Configuration** tab

<img width="1710" alt="Screenshot 2024-11-14 at 6 02 02 PM" src="https://github.com/user-attachments/assets/bccb5970-8b83-4623-b4de-d42deb0948a1">


* Go to **Add-on Settings**. Fill in the details and click **'Save'**

<img width="748" alt="Screenshot 2024-11-18 at 10 59 10 AM" src="https://github.com/user-attachments/assets/1a175c9f-b22b-4be9-be33-d3792a1f3128">



     - Tenant URL: Enter url of Non-employee Risk Management tenant.
     - API Key: Enter SailPoint Non-employee Risk Management API Key.

* Navigate to **Inputs** tab and click on **'Create New Input'**

<img width="1710" alt="Screenshot 2024-11-14 at 6 01 00 PM" src="https://github.com/user-attachments/assets/b7e2ea39-82c6-4dbe-a678-1afdcf87e86e">

   
* Fill in the required details and click **'Add'**

  <img width="800" alt="Screenshot 2024-11-15 at 12 10 29 PM" src="https://github.com/user-attachments/assets/3663b970-b2e8-4455-8d30-624d0698009c">


    - Name: Enter unique name for the data input.
    - Interval: Enter execution interval. Recommendation is 300 seconds (5 minutes).
    - Index: Enter unique index.
    - Tenant Name: Enter name of Non-employee Risk Management tenant.

   

## Usage:

##### Basic Search
 `index=<your_index> sourcetype=<sourcetype_name>`

 <img width="844" alt="Screenshot 2024-11-14 at 12 34 10 PM" src="https://github.com/user-attachments/assets/ac39292b-679a-4829-87ea-b9782f961cd1">




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

* Click on **Import Project**, select the .tgz file in Splunk Add-on Builder.

* Verfiy that the SailPoint Non-employee Risk Management AuditEvent Add-on now appears on main Splunk Dashboard

<img width="269" alt="Screenshot 2024-11-15 at 12 10 13 PM" src="https://github.com/user-attachments/assets/2b33d042-b035-437c-8e21-ca8749b5d61f">



* Edit and Test the add-on
  - Click on the Add-on tile. 
  - Click **'Configure Data Collection'** tab.
  - Click **'Edit'** under **'Actions'**
  - Click **'Next'** button on the top and edit the code.
  - Edit the code in this editor. Use **'Test'** to validate the changes before saving. 
    
    <img width="1710" alt="Screenshot 2024-11-18 at 11 15 02 AM" src="https://github.com/user-attachments/assets/26fde587-b1d0-4dfc-9887-17607eedbd4e">


  - Click **'Save' >> 'Finish'** to save the changes to source type.


## Validate and Package

 Follow instructions : [Validate and Package Add-on using Add-on builder](https://docs.splunk.com/Documentation/AddonBuilder/4.3.0/UserGuide/Validate#:~:text=To%20validate%20your%20add%2Don,and%20and%20display%20the%20results)
 

## License:

This add-on is open-sourced and is distributed under the <license-link>



## Support:

For any issues or questions, please reach out via:

- GitHub Issues:
- Splunk community:








