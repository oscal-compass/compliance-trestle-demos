---
sort-id: ia-05.01
x-trestle-sections:
  guidance: Control Guidance
---

# ia-5.1 - \[Identification and Authentication\] Password-based Authentication

## Control Statement

For password-based authentication:

- \[(a)\] Maintain a list of commonly-used, expected, or compromised passwords and update the list organization-defined frequency and when organizational passwords are suspected to have been compromised directly or indirectly;

- \[(b)\] Verify, when users create or update passwords, that the passwords are not found on the list of commonly-used, expected, or compromised passwords in IA-5(1)(a);

- \[(c)\] Transmit passwords only over cryptographically-protected channels;

- \[(d)\] Store passwords using an approved salted key derivation function, preferably using a keyed hash;

- \[(e)\] Require immediate selection of a new password upon account recovery;

- \[(f)\] Allow user selection of long passwords and passphrases, including spaces and all printable characters;

- \[(g)\] Employ automated tools to assist the user in selecting strong password authenticators; and

- \[(h)\] Enforce the following composition and complexity rules: organization-defined composition and complexity rules.

## Control Control Guidance

Password-based authentication applies to passwords regardless of whether they are used in single-factor or multi-factor authentication. Long passwords or passphrases are preferable over shorter passwords. Enforced composition rules provide marginal security benefits while decreasing usability. However, organizations may choose to establish certain rules for password generation (e.g., minimum character length for long passwords) under certain circumstances and can enforce this requirement in IA-5(1)(h). Account recovery can occur, for example, in situations when a password is forgotten. Cryptographically protected passwords include salted one-way cryptographic hashes of passwords. The list of commonly used, compromised, or expected passwords includes passwords obtained from previous breach corpuses, dictionary words, and repetitive or sequential characters. The list includes context-specific words, such as the name of the service, username, and derivatives thereof.

______________________________________________________________________

## What is the solution and how is it implemented?

<!-- Please leave this section blank and enter implementation details in the parts below. -->

______________________________________________________________________

## Implementation (a)

Add control implementation description here for item ia-5.1_smt.a

______________________________________________________________________

## Implementation (b)

Add control implementation description here for item ia-5.1_smt.b

______________________________________________________________________

## Implementation (c)

Add control implementation description here for item ia-5.1_smt.c

______________________________________________________________________

## Implementation (d)

Add control implementation description here for item ia-5.1_smt.d

______________________________________________________________________

## Implementation (e)

Add control implementation description here for item ia-5.1_smt.e

______________________________________________________________________

## Implementation (f)

Add control implementation description here for item ia-5.1_smt.f

______________________________________________________________________

## Implementation (g)

Add control implementation description here for item ia-5.1_smt.g

______________________________________________________________________

## Implementation (h)

Add control implementation description here for item ia-5.1_smt.h

______________________________________________________________________
