# Commands
`Interface <-- WS --> henChatQ`  
Via JSON.
## Interface -> HCQ
* Online

`{'type': 0x00}`

* Create a new user

```
{
	'type': 0x01,
	'username': 'user name'
}
```

* Send a message

```
{
	'type': 0x02,
	'ch': base64('channel name'),
	'stype': '-t'/'-f'/...,
	'msg': base64('content of the message'),
	'psk': base64('PSK'),
	'qos': 0/1/2
}
```

* Listen on a new channel

```
{
	'type': 0x03,
	'ch': base64('channel name'),
	'psk': base64('PSK')
}
```

## HCQ -> interface
* Online (reply)

```
{
	'type': 0x00,
	'msg': 'welcome message',
	'user': 'user name',
	'chs': {
			base64('ch1'): base64('psk1'),
			base64('ch2'): base64('psk2'),
			...
			},
	'server': 'host:port'
}
```
* New message comes (text)

```
{
	'type': 0x01,
	'ch': base64('channel name'),
	'from': 'sender',
	'time': timeStamp,
	'msg': base64('content of the message'),
	'verified': true / false,
	'timeCheck': true / false
}
```