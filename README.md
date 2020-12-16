# Useful commands#
```shell 
rasa data validate
rasa train
```
Then start the action server:
```shell
rasa run actions
```

Run the dialog in test mode or interactive (learning mode):
```shell
rasa shell  --endpoints endpoints.yml
rasa interactive  --endpoints endpoints.yml
```

# Deployment:
Currently deployed at:
```
http://34.95.33.215/
```
Note: No https!!!

Connect via rest (https://rasa.com/docs/rasa/connectors/your-own-website/)
```
http://<host>:<port>/webhooks/rest/webhook
```