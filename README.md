# BeeBank

BeeBank is a simple banking app, which provide basic operations such as transacrion, fragile data visibility, password change with strength control, transactions list, masked password and account state.

## Some about technology
The main focus when writing this app was safety, so there's loads of elements that guarantee this. \
Firstly, app is written in microservice architecture. It guarantess independence of each component.
There are also this elements:
<ul>
  <li>two step login</li>
  <li>random password when wrong login is provided in first step</li>
  <li>password hashing</li>
  <li>fragile data encryption with AES GCM mode</li>
  <li>jsonschema library</li>
  <li>app gate that redirect requests inside server microservices</li>
  <id>client id used only inside server</id>
  <id>SQL sanitization</id>
  <li>shorted session lifecycle</li>
</ul>
