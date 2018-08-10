# node-red-contrib-google-actionflow
Node Red nodes to receive and respond to Google Action requests from Google Assistant based on actionflow.

Google Assistant is Google's personal assistant that provides the voice recognition and natural language processing behind Google's Android and Home devices.  Google Actions allow you to build conversational agents that interact with the user using a query-response conversation style.

This node is a wrapper around Google's [actions-on-google-nodejs](https://github.com/actions-on-google/actions-on-google-nodejs) client library using the [Actions SDK](https://developers.google.com/actions/reference/nodejs/ActionsSdkApp).

The node runs an Express web server to listen for Action request from Google.  By using a separate web server from Node Red, it allows the node to listen on a different port.  This allows the Action listener to be exposed to the Internet without having the rest of Node Red also exposed.  The web server is required to run HTTPS so you will need SSL certificates. Self signed certificates are OK.

Action requests are received by the Google Action input node and converted into a message.  The message contains some metadata about the conversation and the raw text of the user's input.  State data about the conversation can be passed back and forward to track the state of the conversation.

Once the request has been process, the response is passed to the Google Action Response node which returns it to Google Assistant for delivery to the user.  The response message is contained in msg.payload either as plain text or [Speech Synthesis Markup Language (SSML)](https://developers.google.com/actions/reference/ssml).

A response can either complete the processing of the action or can request further information from the user.

The [action.json](https://github.com/DeanCording/node-red-contrib-google-action/blob/master/action.json) file is used to configure your app on Google Assistant.  The main thing you will need to change is the url of your Node Red server.

To deploy your app, you will need an account on [Google Actions](https://developers.google.com/actions/).  Create a new Dialogflow project in the console and correctly set webhooks.

Be aware that Google Assistant isn't really intended to run private apps.  It is possible to have a private app by keeping your app in test mode perpetually.  One of the difficulties though is that Google requires your app to have a unique name from any other app published by anyone else and you can't use any registered brand name.

Also be aware that there is no security mechanism in this implementation yet.  Google uses [OAuth2.0](https://developers.google.com/actions/identity/oauth2-code-flow) to authorise users to access your end point.  It will be added in a future release (or send me a pull request :-).
