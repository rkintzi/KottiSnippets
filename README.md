<<<<<<< HEAD
KottiSnipplets
==============

This extension allows the end-user (not an administrator / developer) 
to create a small, re-usable pieces of additional content (snippets), 
and associate them with the documents. Currently snippets can be placed
in Kotti slots (on the side panels as well as above and below the 
content). The user can specify the order in which snippets will be 
presented in different slots.


**NOTE! Extension in the early stages of development!** Do not use 
in production systems. In subsequent versions, everything can change, 
=======
KottiSnippets
=============

This extension allows the end-user (not an administrator / developer)
to create a small and re-usable pieces of additional content (snippets),
and to bind them with the documents. Snippets can be placed in Kotti slots
(on the sidebars, above and below the content). The user can specify 
the order in which snippets will be presented in slots.


**NOTE! Extension in the early stages of development!** Do not use 
in production systems. Things will be changed in subsequent versions 
>>>>>>> 79a00f975203e9195649b83c9e1fc8e42c1a422a
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
<<<<<<< HEAD
	kotti_tinymce.kotti_configure 
	kottisnippets.kotti_configure
```

After restarting, the extension will add an additional node (called 
Snippets) under the root of the tree of your documents. To this node, 
users can add snippets. Snippets are created just like any other type 
of content.

After you create snippets, select the document where you want to place 
them and select "Snippets" from the "Acction". You'll see a list of 
available slots to which you can add snippets. To change the order of 
snippets just drag and drop them. You can also delete snippets of 
documents.

License
-------
KottiSnippets is offered under the BSD-derived Repoze Public License.
=======
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
>>>>>>> 79a00f975203e9195649b83c9e1fc8e42c1a422a
