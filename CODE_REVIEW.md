# CODE_REVIEW.md
### Overview
- This file contains a summary of development and changes within the `fix/project-refactor` branch.
- The branch point for `fix/project-origin` started at main SHA: 07a60671479c2885f135b49bdfa1c3b8131505e3.
- This branch took the existing main and integrated it with OpenTAP's boiler plate for Python projects.
- This setup allows users to edit plugin files then test them with `bin\tap editor`.
- This setup allows users to package the plugin with `bin\tap package create ./package.xml`.
- Overall, these changes are preferred for managing dependencies and development.

## Summary 

```diff
  .
+ ├── bin                         # Boiler plate generated, standalone OpenTAP directory for development.
  │   └── ...                   
+ ├── README.md                   # Minor modifications to setup section.
+ ├── UR_Prototype                # New directory for organization.
  │   ├── MoveCobot.py
  │   └── UR3e.py
+ ├── UR_Prototype.Api            # New directory for organization.
+ │   ├── ExampleApi.cs           # Boiler plate generated, not used yet.
+ │   └── UR_Prototype.Api.csproj # Boiler plate generated, necessary for build process.
+ ├── UR_Prototype.sln            # Boiler plate generated, necessary for build process.
+ ├── package.xml                 # Necessary for plugin package generation.
- └── requirements.txt            # No longer necessary, removed.
```