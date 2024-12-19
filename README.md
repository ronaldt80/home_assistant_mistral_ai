<h1>Mistral AI Integration in Home Assistant</h1>

This is a custom integration for home assistant which will allow you to send prompts to mistral ai.

<h2>Use-Cases</h2>
<lu>
  <li>Let mistral ai decide wether you should open the windows. Send the outside temperature and humidity to mistral ai along with the avarage temperature and humidity of all your rooms.</li>
  <li>Get dynamic push notifications created by the AI instead of the same static sentences you normall define.</li>
  <li>Feed mistral ai with your workout data to get a quick summary</li>
</lu>

<h2>Requirements</h2>
You will need to have an account with mistral ai (its free) and also need to sign-up for an api-key (also free).
If you wish to use agents you'll also have to define agents on thei developer portal.

<a href="https://mistral.ai/">Mistral AI<a>

<h3>Installation</h3>

Add the following to your configuration.yaml

    mistral_ai_api:
      name: "Mistral AI API"
      api_key: !secret mistral_token

Then add a entry of "mistral_token" to your secrets.yaml. This is where your API-Key goes


<h4>How to use</h4>
The integration offers two parts

1. A service called mistral_ai_api.send_prompt
2. A event with the identifier <b>mistral_ai_response</b>


You can call the send_prompt-command like this

    action: mistral_ai_api.send_prompt
    metadata: {}
    data:
      prompt: Whats the weather
      identifier: my-question-123


This will send the prompt to mistral ai.
Once mistral ai sent back the response the mentioned event will be thrown.

You can react to that in an automation and do whatever you want with the result

    alias: "[Mistral AI] React on mistral ai response"
    description: ""
    triggers:
      - trigger: event
        event_type: mistral_ai_response
    conditions: []
    actions:
      - action: notify.mobile_app_iphone_5
        metadata: {}
        data:
          message: >-
            {{trigger.event.data.identifier}} - {{trigger.event.data.agent_id}} -
            {{trigger.event.data.response}}
    mode: single


As you can see the mistral_ai_api.send_prompt takes additional (optional) arguments

<table>
<tr>
	<td>prompt</t>
	<td>The prompt to send to mistral</td>
<tr>
<tr>
	<td>agent_id</t>
	<td>(optional) The id of an agent you want to utilize
<tr>
<tr>
	<td>identifier</t>
	<td>(Optional) A custom identifier which will be returned in the event so you know which prompt the answer belonged to</td>
<tr>
</table>

<h5>Disclaimer</h5>
This is my first home assistant integration and I have zero experience in developing for home assistant. I am sure things could be done way better... but I have no idea how.
If anybody wants to help with this or would like to offer some advice I'd be happy to accept it.

<h5>Things to add</h5>
* Allow for selection a specific mistral ai model
* Lots more... have to read their documentation
