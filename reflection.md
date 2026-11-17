# SOAP Client API Development — Reflection

The biggest challenge I encountered during this assignment wasn't writing the Flask endpoints or implementing validation. It was getting the SOAP service to communicate with my application. I initially used a NumberConversion service, but every request failed because the remote server kept closing or resetting the connection. I tried different URLs, tested the WSDL directly with Zeep, and even used curl to determine whether the issue was with my code or the external service.

Eventually, I switched to the CountryInfoService, which allowed me to retrieve country information using two-letter ISO codes. From there, I implemented GET and POST endpoints and added validation to reject incorrectly formatted country codes.

Testing both endpoints helped me understand how SOAP and REST can work together. My Flask application accepts straightforward HTTP requests while Zeep handles communication with the SOAP service behind the scenes. I also learned why meaningful error messages are important when an application depends on external services.