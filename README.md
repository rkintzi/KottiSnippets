KottiSnippets
=============

This extension allows the end-user (not an administrator / developer)
to create a small and re-usable pieces of additional content (snippets),
and to bind them with the documents. Snippets can be placed in Kotti slots
(on the sidebars, above and below the content). The user can specify 
the order in which snippets will be presented in slots.


**NOTE! Extension in the early stages of development!** Do not use 
in production systems. Things will be changed in subsequent versions 
without concern for backwards compatibility.

Installation
------------

As usual:


```
$ python setup.py develop
```

Then change the ```kotti.configurators``` setting in your INI file. 
For example:

```
kotti.configurators = 
  kotti_tinymce.kotti_configure 
	kottisnippets.kotti_configure
```

Usage
-----

First time you run your site with the extension enabled, it will add 
an additional node (called Snippets) under the root of the tree of your 
documents. You can add snippets to this node. Snippets are created just 
like any other type of content.

When snippets are already created, navigate to the document with which 
you want them to be bound. Select "Snippets" from menu "Actions" 
and you will see list of available slots. If there are Snippets already
bound with document they are listed as well. Here you may add, remove 
and reorder (just drag and drop) snippets.

License
-------
KottiSnippets is offered under the BSD-derived Repoze Public License.