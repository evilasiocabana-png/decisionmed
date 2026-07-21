# DM-070 — Safe workflow DOM rendering

The specialty workflow no longer uses HTML string injection to add the optional PsychRx link in the structural review view. The link is created with DOM APIs and cleared before every render.

This is a frontend hardening change only. It does not change workflow APIs, session progression, reference-only data boundaries or clinical permissions.

The MVP shell test now confirms that the workflow page contains no `innerHTML` use.
