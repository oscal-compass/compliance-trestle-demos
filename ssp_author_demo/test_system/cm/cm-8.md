---
sort-id: cm-08
x-trestle-sections:
  guidance: Guidance
---

# cm-8 - \[Configuration Management\] System Component Inventory

## Control Statement

- \[a.\] Develop and document an inventory of system components that:

  - \[1.\] Accurately reflects the system;
  - \[2.\] Includes all components within the system;
  - \[3.\] Does not include duplicate accounting of components or components assigned to any other system;
  - \[4.\] Is at the level of granularity deemed necessary for tracking and reporting; and
  - \[5.\] Includes the following information to achieve system component accountability: organization-defined information deemed necessary to achieve effective system component accountability; and

- \[b.\] Review and update the system component inventory organization-defined frequency.

## Control Guidance

System components are discrete, identifiable information technology assets that include hardware, software, and firmware. Organizations may choose to implement centralized system component inventories that include components from all organizational systems. In such situations, organizations ensure that the inventories include system-specific information required for component accountability. The information necessary for effective accountability of system components includes the system name, software owners, software version numbers, hardware inventory specifications, software license information, and for networked components, the machine names and network addresses across all implemented protocols (e.g., IPv4, IPv6). Inventory specifications include date of receipt, cost, model, serial number, manufacturer, supplier information, component type, and physical location.

Preventing duplicate accounting of system components addresses the lack of accountability that occurs when component ownership and system association is not known, especially in large or complex connected systems. Effective prevention of duplicate accounting of system components necessitates use of a unique identifier for each component. For software inventory, centrally managed software that is accessed via other systems is addressed as a component of the system on which it is installed and managed. Software installed on multiple organizational systems and managed at the system level is addressed for each individual system and may appear more than once in a centralized component inventory, necessitating a system association for each software instance in the centralized inventory to avoid duplicate accounting of components. Scanning systems implementing multiple network protocols (e.g., IPv4 and IPv6) can result in duplicate components being identified in different address spaces. The implementation of [CM-8(7)](#cm-8.7) can help to eliminate duplicate accounting of components.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- Please leave this section blank and enter implementation details in the parts below. -->

______________________________________________________________________

## Implementation a.

Add control implementation description here for item cm-8_smt.a

______________________________________________________________________

## Implementation b.

Add control implementation description here for item cm-8_smt.b

______________________________________________________________________
