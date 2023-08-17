# FacebookMessengerRefBot

This is an example bot that that uses a custom lifecycle event to "silence" the bot for specific Facebook Messenger ref links.

## Resources
- https://developers.facebook.com/docs/messenger-platform/discovery/m-me-links/
- https://developers.facebook.com/docs/messenger-platform/discovery/welcome-screen
- https://github.com/meya-customers/demo-app
- https://docs.meya.ai/docs/facebook-messenger

## Example ref links
Bot responds:
https://m.me/meya.goodunitedbot?ref=meya

Bot won't respond:
https://m.me/meya.goodunitedbot?ref=manychat

## Key steps
1. Remove sensitive data integration
2. Add custom MeyaFlowElement log element 
   1. emits lifecycle
   2. includes ref
   3. identify thread and user
3. Create a lifecycle id flow that programmatically pauses/unpauses bot based on postback ref
