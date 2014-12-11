Kiloblog
========
data model
----------
The data model is implemented in sqlalchemy. It consists of two tables, the
`chapters` table, which handles the many-to-many prequels and sequels
relationship and the `post` table, which handles the content.

### chapters ###

{{ d['kiloblog.py']['chapters'] }}

The `chapters` table simply consists of the relationships between prequels and
sequels. This relationship is determined by the `post.id`, so changes in the
title should not effect it.

### Post ###

{{ d['kiloblog.py']['Post'] }}

The `Post` table consists of the id, title, content and a relationship with the
chapters table for prequels and sequels.

**TODO:** This is lacking a few fields, specifically:

 - Author
 - Publication date
 - Draft status

views
-----

**TODO:** Really, the index should only list the latest few stories or latest
one, just like http://ficlet.com used to. The edit/new methods should probably
be integrated into a single view as well.

### index ###

{{ d['kiloblog.py']['index'] }}

The index has a form to post a new story. It also renders all the current
stories in the system.

### show ###

{{ d['kiloblog.py']['show'] }}

This view shows a single post.

### edit ###

{{ d['kiloblog.py']['edit'] }}

This view allows for editing of a post.
