<h1>Project Utils/Setup</h1>
<p>make infra-dev-setup</p>
 <ul>
  <li>sets up a local neo4j instance</li>
  <li>TODO: sets up a local document database instance</li>
</ul>
<p>make infra-dev-clean</p>
 <ul>
  <li>tears down and cleans up local dev infra</li>
</ul>  
<p>go run cmd/myapp/main.go</p>
 <ul>
  <li>runs app</li>
</ul>  

<h1>Data Structure</h1>
<p>Functionalities of the app can be found in the ./pkg directory</p>
 <ul>
  <li>Functionality is centered on the user</li>
  <li>Each library besides 'user' exposes an engine which when called with user specific info generates a document stored in the db that contains the view of data important to the user</li>
  <li>All persistent data about users is stored in the graph database, each library's engine uses this data to generate its view document for the user</li>
</ul>  