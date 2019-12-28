# Usage
## Setup
Fill in the following values with your information:
 - `domain`: The domain/zone you wish to update
 - `subdomains`: List of A records that you wish to update, specified using subdomain.<br/>
      E.G: for the record `test.example.com`, you would enter `test`. For the top-level domain, enter a blank string
 - `X-Auth-Email`: The email associated with your Cloudflare account
 - `X-Auth-Key`: You account's API key
 
 ## Operation
 Now just run the code normally. If it has issues with updating a record, it will try up to 5 times. The loop will timeout after 5 minutes should it get stuck.
 
 # Issues
 While the code *should* be fine (I use it), it may cause unexpected issues. If you detect one, please raise an issue so it can be fixed.
 
