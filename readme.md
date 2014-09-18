KiloBlog
========
A blog engine written in 1024 bytes (or less). Currently at TBD/1024

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
 - Make a Post
 - View Posts
 - Edit Post
 - Delete Post
 - Add Sequel

Test Results
------------
{{d['runtests.py|py']}}

dexy notes
----------
 - Markdown filter does not work without jinja in-between filename and filter
 - Dexy files are executed in copied directory, not working directory. Makes
   extracting test results a bit of a pain.
