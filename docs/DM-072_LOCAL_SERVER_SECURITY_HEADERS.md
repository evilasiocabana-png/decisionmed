# DM-072 — Local server security headers

Every response served by the DecisionMEd local hub now carries browser security headers:

- content-type sniffing is disabled;
- framing and referrer disclosure are blocked;
- browser access to camera, microphone and geolocation is denied;
- the content security policy limits resources and connections to the local origin.

The CSP explicitly permits the current inline styles and scripts required by the static reference workspace. This does not expose the loopback server to the network and does not alter clinical permissions or data handling.
