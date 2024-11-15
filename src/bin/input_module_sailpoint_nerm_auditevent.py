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


# Function to test if the url is https.
def is_https(helper, nerm_url):
    helper.log_info("INFO Entering is_https().")
    scheme = urlparse(nerm_url).scheme
    if scheme.lower() == 'https':
        helper.log_info("INFO NERM URL is HTTPS.")
        return True
    else:
        helper.log_error("ERROR NERM URL is not HTTPS.")
        return False


# Function to build a header for NERM requests.
def build_header(helper, api_key):
    helper.log_info("INFO Entering build_header().")
    if api_key:
        # If api_key exists then construct auth.
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
    helper.log_info("INFO Entering get_checkpoint_time().")
    content = [x.strip() for x in content]

    checkpoint_time = None
    # Set checkpoint time to what was saved in the checkpoint file
    if len(content) == 1:
        checkpoint_time = content[0]
    return checkpoint_time


# Function to get audit events response.
def get_nerm_audit_events_response(
        helper, nerm_audit_events_url, headers, query_params, search_payload, use_proxy
):
    helper.log_info("INFO Entering get_nerm_audit_events_response().")

    # Check if nerm_audit_events_url is https.
    if not is_https(helper, nerm_audit_events_url):
        helper.log_info("INFO Search Events URL is not HTTPS.")
        return False

    response = helper.send_http_request(
        nerm_audit_events_url,
        "POST",
        parameters=query_params,
        payload=search_payload,
        headers=headers,
        cookies=None,
        verify=True,
        cert=None,
        timeout=None,
        use_proxy=use_proxy,
    )

    return response


# Function to construct payload.
def build_search_payload(helper, limit, checkpoint_time=None):
    helper.log_info("INFO Entering build_search_payload().")

    # Search criteria - retrieve all audit events since the checkpoint time, sorted by created date
    search_payload = {
        "audit_events": {
            "sort": "created_at",
            "limit": limit,
            "order": "asc",
            "filters": {
                "subject_type": "Profile",
            },
        }
    }
    if checkpoint_time:
        search_payload['audit_events']['filters']["created_at"] = {"gt": f"{checkpoint_time}"}

    return search_payload


# Function to construct query parameters.
def build_query_params(helper):
    helper.log_info("INFO Entering build_query_params().")
    query_params = {"metadata": True}

    return query_params


def validate_input(helper, definition):
    helper.log_info("INFO Entering validate_input().")
    pass


def collect_events(helper, ew):
    helper.log_info("INFO Entering collect_events().")

    # Get information about NERM from the input configuration
    # Information on how to attain these values can be found on community.sailpoint.com

    tenant_name = helper.get_arg("tenant_name")
    tenant_url = helper.get_global_setting("tenant_url")
    api_key = helper.get_global_setting("api_key")

    nerm_audit_events_url = "{}/api/audit_events/query".format(tenant_url)

    # Check if nerm_audit_events_url is https.
    if not is_https(helper, nerm_audit_events_url):
        return False

    # Read the timestamp from the checkpoint file, and create the checkpoint file if necessary The checkpoint file
    # contains datetime of 'created_at' field of the last event seen in the previous execution of the
    # script.
    checkpoint_file = os.path.join(os.environ['SPLUNK_HOME'], 'etc', 'apps',
                                   'TA-sailpoint-nerm-auditevent-add-on', 'tmp',
                                   tenant_name + "_checkpoint.txt")
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

    audit_events = []
    partial_set = False

    # Number of Events to return per call to the search API
    limit = 100  # Max number of results to return. Default is 100.
    new_checkpoint_time = None

    while True:

        if partial_set == True:
            break

        # Get the query parameters.
        query_params = build_query_params(helper)

        # Search criteria - retrieve all audit events since the checkpoint time, sorted by created date.
        search_payload = build_search_payload(helper, limit, checkpoint_time)

        # Initiate request
        response = get_nerm_audit_events_response(helper, nerm_audit_events_url, headers, query_params, search_payload,
                                                  use_proxy)

        if response.ok:
            resp_obj = response.json()
            if resp_obj is not None:

                x_total_count = len(resp_obj["audit_events"])
                try:
                    if x_total_count < limit:
                        # less than limit returned, caught up so exit
                        partial_set = True

                    # Add this set of results to the audit events array

                    audit_events.extend(resp_obj["audit_events"])

                    current_last_event = audit_events[-1]
                    checkpoint_time = current_last_event["created_at"]

                except KeyError:
                    helper.log_error("Response does not contain items")
                    break
        else:
            helper.log_error("Failure from server" + str(response.status_code))
            # hard exit
            return 0

    # Iterate the audit events array and create Splunk events for each one
    if len(audit_events) > 0:

        for audit_event in audit_events:
            data = json.dumps(audit_event)
            event = helper.new_event(data=data, time=None, host=tenant_name, index=helper.get_output_index(),
                                     source=helper.get_input_type(), sourcetype=helper.get_sourcetype(), done=True,
                                     unbroken=True)
            ew.write_event(event)

        # Get the created date of the last AuditEvent in this run and save it as the checkpoint time in the
        # checkpoint file
        new_checkpoint_time = audit_events[-1]["created_at"]

    # Write new checkpoint time back to checkpoint file
    if new_checkpoint_time:
        with open(checkpoint_file, "r+") as f:
            f.seek(0)
            f.write(str(new_checkpoint_time))
            f.truncate()
