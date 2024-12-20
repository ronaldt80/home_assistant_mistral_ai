<h1>Mistral AI Integration in Home Assistant</h1>

This is a custom integration for home assistant which will allow you to send prompts to mistral ai.

<h2>Use-Cases</h2>
<lu>
  <li>Let mistral ai decide wether you should open the windows. Send the outside temperature and humidity to mistral ai along with the avarage temperature and humidity of all your rooms.</li>
  <li>Get dynamic push notifications created by the AI instead of the same static sentences you normall define.</li>
  <li>Feed mistral ai with your workout data to get a quick summary</li>
</lu>

<h2>Example code</h2>

<b>Script to send prompt to mistral</b>
	
	action: mistral_ai_api.send_prompt
	metadata: {}
	data:
	  identifier: Rückgabe
	  model: mistral-large-latest
	  prompt: >-
	    I'm thinking bout wether I should ventilate my home. The outside temperature
	    is     {{state_attr('weather.forecast_home','temperature')}} degree and the
	    outside humdity is      {{state_attr('weather.forecast_home','humidity')}}%.
	    The avarage temperature of all my rooms is            
	    {{states('sensor.durchschn_temperatur_in_der_wohnung')}} degree and the
	    avarage humidity of all my rooms is         
	    {{states('sensor.durchschn_feuchtigkeit_in_der_wohnung')}}%. Should I
	    ventilate? Explain your reasoning.

<b>Automation to react to response event</b>

	alias: "[Mistral AI] React on mistral ai response"
	description: ""
	triggers:
	  - trigger: event
	    event_type: mistral_ai_response
	conditions: []
	actions:
	  - action: persistent_notification.create
	    metadata: {}
	    data:
	      message: "{{trigger.event.data.response}}"
	mode: single

<b>AI response</b>

	To determine whether you should ventilate your home, it’s important to consider the effects of temperature and humidity on indoor air quality and comfort. Here’s a breakdown of your situation:

	Outside Conditions:
	Temperature: 2.3°C
	Humidity: 89%
	Inside Conditions:
	Temperature: 18.5°C
	Humidity: 57%
	Key Considerations:
	Temperature Difference:
	The outside temperature is significantly lower than the inside temperature. Ventilating by opening windows could lead to a drop in indoor temperature, making the environment colder.
	Humidity Levels:
	The outside humidity is much higher than the inside humidity. Introducing this high humidity into your home could increase the indoor humidity levels, which might lead to discomfort and potential issues like condensation and mold growth.
	Indoor Air Quality:
	Ventilation helps to reduce indoor pollutants, odors, and carbon dioxide levels, improving overall air quality. However, it should be balanced with maintaining comfortable temperature and humidity levels.
	Recommendations:
	Given the significant difference in temperature and humidity, it might not be the best time to ventilate your home by simply opening windows. Here are some alternative suggestions:
	
	Mechanical Ventilation:
	If your home has a mechanical ventilation system (e.g., heat recovery ventilator), use it. These systems can exchange indoor and outdoor air while maintaining temperature and humidity levels.
	Short Bursts of Ventilation:
	Open windows for short periods (e.g., 5-10 minutes) to allow for some air exchange without drastically affecting the indoor temperature and humidity.
	Monitor Indoor Air Quality:
	Use indoor air quality monitors to check levels of pollutants, carbon dioxide, and humidity. This can help you decide when ventilation is necessary.
	Use Dehumidifiers:
	If you decide to ventilate and notice an increase in indoor humidity, consider using a dehumidifier to maintain comfortable levels.
	Conclusion:
	Based on the current conditions, it might be better to avoid prolonged ventilation by opening windows. Instead, consider using mechanical ventilation or short bursts of ventilation to maintain indoor air quality without compromising comfort.

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

Or like this
	
	action: mistral_ai_api.send_prompt
	    metadata: {}
	    data:
	      	prompt: Give me a jinja2 template to show some data in a nice formatted way. Make sure to only return the code as-is so I can use it directly in a markdown. Don't add any explanation, just return the code.
       		model: codestral-latest
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
	<td>model</t>
	<td>The mistral ai model to be used. Not required when using an agent</td>
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
* <del>Allow for selection a specific mistral ai model</del> (Done)<br/>
* Lots more... have to read their documentation
