KiloBlog
========
A blog engine written in 1024 bytes of minified, gzipped python code. All other
content needs to be one kilobyte or less per file.

So this basically means:

 - Python code (not including configurat) 1024 minified + gzipped
 - each html file 1024 minifed + gzipped
 - site CSS 1024 minified + gzipped
 - js library 1024 minified + gzipped
 - site js 1024 minified + gzipped
 - CSS framework 1024 minified + gzipped

Anything not in the list (e.g. tests, documentation, initial data) do not have
that limit.

{{ d['sizes.sh|shint']|indent(indentfirst=true) }}

Tasks
-----
 - Better testing tools
 - Metrics integrated into this document
 - PDF output of this document
 - External configuration (external configuraiton definitely does not count against line limit)

Constraints
-----------
 - All libraries used must be general use and published to PyPI.
 - The kilobyte limitation is for source code, not for assets, input data, etc.
 - Everything is documented, literate programming style, with dexy
 - Test results are colorized and pretty and also integrated, possibly with
   metrics.

Feature Ideas
-------------
 - Character limit on posts of 1024
 - Tagging
 - Rating
 - Mozilla Persona
 - Sandboy?
### Sequels/threads (Ficlet!) ###
 - Input: Users select millific to sequel or prequel by clicking "Make sequel"
   or "Make prequel" link, new form opens up that has a prepopulated hidden
   field or maybe a sub URL for that specific story.
 - Prequels and sequels are listed on the page for the story.

Story Map
---------
 - User Registration
 - User Login
 - [DONE] <s>Make a Post</s>
 - [DONE] <s>View Posts</s>
 - [DONE] <s>Edit Post</s>
 - Delete Post
 - Add Sequel

Design
------
Adjacency List Relationships

dexy notes
----------
 - Markdown filter does not work without jinja in-between filename and filter
 - Dexy files are executed in copied directory, not working directory. Makes
   extracting test results a bit of a pain. -- This can be changed with a dexy
   setting.
