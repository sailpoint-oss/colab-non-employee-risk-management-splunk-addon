# encoding = utf-8

import datetime
import json
import os
import time
from urllib.parse import urlparse

'''
    IMPORTANT
    Edit only the validate_input and collect_events functions.
    Do not edit any other part in this file.
    This file is generated only once when creating the modular input.
'''


# This method will determine if the current timestamp should be used instead of the value stored in the checkpoint
# file. Will return 'true' if the checkpoint time is 1 or more days in the past.
def use_current(now, old):
    ret = False

    try:
        current_time = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        current_time = datetime.datetime.strptime(now, '%Y-%m-%dT%H:%M:%SZ')

    try:
        old_time = datetime.datetime.strptime(old, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        old_time = datetime.datetime.strptime(old, '%Y-%m-%dT%H:%M:%SZ')

    diff = current_time - old_time
    delta_days = diff.days

    if int(delta_days) > 0:
        ret = True

    return ret


# Function to test if the url is https.
def is_https(helper, nerm_url):
    scheme = urlparse(nerm_url).scheme
    if scheme.lower() == 'https':
        helper.log_info("INFO NERM URL is HTTPS.")
        return True
    else:
        helper.log_error("ERROR NERM URL is not HTTPS.")
        return False


# Function to build a header for NERM requests.
def build_header(helper, api_key):
    if api_key:
        # If NERM url and api_key exists then construct oauth.
        return {
            'Authorization': 'Bearer ' + api_key,
            'Content-Type': 'application/json'
        }
    else:
        # This should not happen.
        helper.log_error("Error No credentials were provided.")
        return None


# Function to get checkpoint time.
def get_checkpoint_time(helper, content):
    content = [x.strip() for x in content]
    helper.log_info(f"content: {content}")
    # need to operate on a 5-minute delay
    new_checkpoint_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=60)).isoformat() + "Z"

    # Set checkpoint time to either the current timestamp, or what was saved in the checkpoint file
    if len(content) == 1:
        checkpoint_time = content[0]
        if use_current(new_checkpoint_time, checkpoint_time):
            checkpoint_time = new_checkpoint_time
            return checkpoint_time
        return checkpoint_time
    else:
        checkpoint_time = new_checkpoint_time
        return checkpoint_time


# Function to get audit events response.
def get_search_events_response(helper, audit_events_url, headers, search_payload, use_proxy):
    # Check if search_events_url is https.
    if not is_https(helper, audit_events_url):
        helper.log_info("INFO Search Events URL is not HTTPS.")
        return False

    response = helper.send_http_request(audit_events_url, "POST", payload=search_payload,
                                        headers=headers, cookies=None, verify=True, cert=None, timeout=None,
                                        use_proxy=use_proxy)

    return response


# Function to construct payload.
def build_search_payload(helper, checkpoint_time):
    # Search API results are slightly delayed, allow for 5 minutes though in reality
    # this time will be much shorter. Cap query at checkpoint time to 5 minutes ago

    if checkpoint_time is None or checkpoint_time == "":
        return None

    search_delay_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=60)).isoformat() + "Z"

    query_checkpoint_time = checkpoint_time.replace('-', '\\-').replace('.', '\\.').replace(':', '\\:')
    query_search_delay_time = search_delay_time.replace('-', '\\-').replace('.', '\\.').replace(':', '\\:')

    helper.log_info(f'checkpoint_time {query_checkpoint_time} search_delay_time {query_search_delay_time}')

    # Search criteria - retrieve all audit events since the checkpoint time, sorted by created date
    search_payload = {
        "audit_events": {
            "filters": {
                "subject_type": "Profile",
                "created_at":f">{query_checkpoint_time} AND created:<{query_search_delay_time}"
            },
            "limit": 100,
            "sort": "created_at",
            "order": "asc"
        }
    }

    return search_payload


# Function to construct query parameters.
def build_query_params(count, limit, offset):
    max_limit = 10000
    if not offset or offset < 0:
        offset = 0

    if not limit or limit > max_limit:
        limit = max_limit

    query_params = {
        "count": count,
        "offset": offset,
        "limit": limit
    }

    return query_params


def validate_input(helper, definition):
    pass


def collect_events(helper, ew):
    # Get information about NERM from the input configuration
    # Information on how to attain these values can be found on community.sailpoint.com

    org_name = helper.get_global_setting('organization_name')
    nerm_url = 'https://{}.seczetta.com/api'.format(org_name)
    api_key = helper.get_global_setting('api_key')


    # Check if nerm_url is https.
    if not is_https(helper, nerm_url):
        return False

    # Read the timestamp from the checkpoint file, and create the checkpoint file if necessary The checkpoint file
    # contains the ISO datetime of the 'created' field of the last event seen in the previous execution of the
    # script. If the checkpoint time was greater than a day in the passed, use current datetime to avoid massive load
    # if search disabled for long period of time Note the filename is prepended with the clientId value, so a new or
    # different client will have a different checkpoint file

    checkpoint_file = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps',
                                   'TA-sailpoint-nerm-auditevent-add-on', 'tmp',
                                   org_name + "_checkpoint.txt")
    try:
        file = open(checkpoint_file, 'r')
    except IOError:
        try:
            file = open(checkpoint_file, 'w')
        except IOError:
            os.makedirs(os.path.dirname(checkpoint_file))
            file = open(checkpoint_file, 'w')

    with open(checkpoint_file) as f:
        content = f.readlines()

    checkpoint_time = get_checkpoint_time(helper, content)

    # PROXY SETTINGS
    use_proxy = True if helper.get_proxy() else False

    # Build the header.
    headers = build_header(helper, api_key)
    print(f"Headers: {headers}")

    audit_events = []
    partial_set = False

    # Number of Events to return per call to the search API
    limit = 10000  # Max number of results to return. Default is 250.
    count = "true"
    offset = 0

    while True:

        if partial_set == True:
            break

        # Get the query parameters.
        query_params = build_query_params(count, limit, offset)
        helper.log_error(f"query_params: {query_params}")
        # Search criteria - retrieve all audit events since the checkpoint time, sorted by created date.
        search_payload = build_search_payload(helper, checkpoint_time)
        helper.log_error(f"search_payload: {search_payload}")
        # audit events url
        audit_events_url = nerm_url + "/audit_events/query"
        helper.log_error(f"audit_events_url: {audit_events_url}")

        # Initiate request
        response = get_search_events_response(helper, audit_events_url, headers, search_payload,
                                              use_proxy)

        # API Gateway saturated / rate limit encountered. Delay and try again.
        # Delay will either be dictated by NERM server response or 5 seconds
        if response.status_code == 429:

            retryDelay = 5
            retryAfter = response.headers['Retry-After']
            if retryAfter is not None:
                retryDelay = 1000 * int(retryAfter)

            helper.log_warning("429 - Rate Limit Exceeded, retrying in " + str(retryDelay))
            time.sleep(retryDelay)

        elif response.ok:

            if response.json() is not None:
                try:
                    partial_set = True
                    results = response.json()
                    # Add this set of results to the audit events array
                    audit_events.extend(results['audit_events'])
                    checkpoint_time = audit_events[-1]["created_at"]
                except KeyError:
                    helper.log_error("Response does not contain items")
                    break
        else:
            helper.log_error("Failure from server" + str(response.status_code))
            # hard exit
            return 0
    new_checkpoint_time = (datetime.datetime.utcnow() - datetime.timedelta(minutes=60)).isoformat() + "Z"


    # Iterate the audit events array and create Splunk events for each one
    if len(audit_events) > 0:
        for audit_event in audit_events:
            data = json.dumps(audit_event)
            event = helper.new_event(data=data, time=None, host=nerm_url, index=helper.get_output_index(),
                                     source=helper.get_input_type(), sourcetype=helper.get_sourcetype(), done=True,
                                     unbroken=True)
            ew.write_event(event)

        # Get the created date of the last AuditEvent in this run and save it as the checkpoint time in the
        # checkpoint file
        new_checkpoint_time = audit_events[-1]["created_at"]

    # Write new checkpoint time back to checkpoint file
    with open(checkpoint_file, 'r+') as f:
        f.seek(0)
        f.write(str(new_checkpoint_time))
        f.truncate()
