# CG Python Multi-file Script

Simple script to collect python class definitions across multiple files with `build <file>`.

## Installation:

Install it by downloading the package from 
 ``github`` and running ``pip install <folder where cg_py_class_merger is located>``

## Sample Workflow:
**Project structure:**

    codingame/

        lib/
            __init__.py
            your_package_folder_1/
               __init__.py
               package_1.py
     
            your_package_folder_2/
               __init__.py
               package_2.py

            cg_py_class_merger/
               cg_py_class_merger/
                  __init__.py
                  build.py
               README.md
               setup.py

        
        any_project/ # for example 'ClashOfCodes'

example:

      # IMPORT
      from lib.your_package_folder_1.package_1.py import *
      # END_IMPORT

Do not forget to init your packages with ``__init__.py``

In ``any_project`` folder (ClashOfCodes for example) simply run ``build <filename>.py``, or define a file watcher in your IDE.

PyCharm config for file watcher:

    <?xml version="1.0" encoding="UTF-8"?>
    <project version="4">
      <component name="ProjectTasksOptions">
        <TaskOptions isEnabled="true">
          <option name="arguments" value="$FileName$" />
          <option name="checkSyntaxErrors" value="true" />
          <option name="description" />
          <option name="exitCodeBehavior" value="ALWAYS" />
          <option name="fileExtension" value="py" />
          <option name="immediateSync" value="true" />
          <option name="name" value="CG_merger" />
          <option name="output" value="" />
          <option name="outputFilters">
            <array />
          </option>
          <option name="outputFromStdout" value="false" />

Output will be ``cg.py`` in your ``any_project`` folder

Examples:

https://github.com/zolcsika71/CodeInGames_PY

https://github.com/zolcsika71/CodeInGames_PY/tree/main/merge_test

https://github.com/zolcsika71/CodeInGames_PY/tree/main/ClashOfCodes

## Issues

1. Generate dependency tree and resolve order of imports automatically
