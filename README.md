KiloBlog
========
A blog engine written in 1024 bytes of minified, gzipped code. Currently at...

{{ d['sizes.sh|shint']|indent(indentfirst=true) }}

Tasks
-----
 - Better testing tools
 - Metrics integrated into this document
 - PDF output of this document
 - Decision on metrics -- gzip, include HTML/external files?
   - Perhaps just count file and each file is under 1 KB in size will be sufficient
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
 - Sequels/threads (Ficlet!)
 - Tagging
 - Mozilla Persona
 - Sandboy?

Outs
----
If this is too hard of a constraint, here are some other possible solutions:
 - Each file is 1024 or less, minimize the number of files
 - 1024 compressed
 - 1024 python only

Story Map
---------
 - User Registration
 - User Login
 - [DONE] <s>Make a Post</s>
 - [DONE] <s>View Posts</s>
 - [DONE] <s>Edit Post</s>
 - Delete Post
 - Add Sequel

dexy notes
----------
 - Markdown filter does not work without jinja in-between filename and filter
 - Dexy files are executed in copied directory, not working directory. Makes
   extracting test results a bit of a pain. -- This can be changed with a dexy
   setting.
