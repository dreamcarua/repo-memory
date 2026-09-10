# <Project> — traps

Read before the first edit of code or config. Add an entry whenever something cost more than 15 minutes of surprise, in the same commit as the fix.

<!--
Format:
### Short name of the trap
**Symptom:** what you will see.
**Cause:** why it happens.
**Do:** the concrete action.
**Seen:** DD.MM.YYYY

Twelve classes worth looking for on purpose: several layers of the same thing (cache, copies, mirrors) · hidden execution order · a whole that breaks when a part is removed · silent loss in a named-field list · identifier without uniqueness guarantee · value without its unit · two implementations of the same logic · a default that points elsewhere · deploy resets what you did not mention · empty result of a narrowed filter · cache whose key does not contain what you changed · dormant defect woken by a change in data shape.
-->

_Nothing recorded yet._

Delete that line when you add the first trap; the format is in the comment above. An empty entry
skeleton is worse than an empty file, because a later session reads it as a trap somebody started
writing down and abandoned.
