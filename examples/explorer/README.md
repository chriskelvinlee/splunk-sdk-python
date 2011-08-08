The 'explorer' example is a browser-based API explorer. It is keyed of the same
data that generates the Splunk REST reference docs, and so is meant to be
authoritative.

To run, simply execute:
    ./explorer.py

It will pick up all relevant values from your .splunkrc, or you can pass them 
in on the command line. You can see help by adding '--help' to the exectuion.

The API Explorer will open up a browser window that will show you a drop down
for all the Splunk REST APIs, as well as server configuration information
to know which server to connect to.

Once an API is chosen, a API-specific form will be created that will allow you
to fill in all the parameters required by the specific API. It will also
validate that all required parameters are present. 

When the API call is made, it will issue a call to the Splunk server (through a
locally hosted redirect server to work around cross-domain issues), and display
the response it received.

FUTURE WORK
-----------

- Switch to JSONP once the server supports it
- Validate parameter types (int, string, enum, etc)