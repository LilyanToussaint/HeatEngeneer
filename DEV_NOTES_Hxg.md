# Notes de conception pour le futur module `Source/Hxg`

Le package `Source/Hxg` servira de couche d'agrégation au-dessus des briques
utilitaires génériques. Il orchestrera les fluides, matériaux, corrélations
HTC/Δp et les futures géométries pour proposer des modèles d'échangeurs
complets (ε-NTU, LMTD, instationnaire, etc.).

## Dépendances prévues

Le module `Hxg` consommera exclusivement les packages suivants :

- `Source.Fluid` pour la représentation des fluides (classe `CoolPropFluid`).
- `Source.materials` pour les matériaux de paroi (classe `Material` + base de données).
- `Source.util` pour les grandeurs de base (Re, Pr, conversions débit ↔ vitesse).
- `Source.Heat_transfer_coefficient` pour les calculs de coefficients h.
- `Source.loss_pressure` pour les modèles de pertes de charge.

Règle importante : **aucun module en dehors de `Hxg` ne doit importer `Hxg`.**
Cette couche reste au sommet de la hiérarchie et encapsule les briques
élémentaires sans introduire de dépendance circulaire.

Les fichiers actuellement présents dans `Source/Hxg/` sont des squelettes. Ils
seront complétés lors des phases ultérieures (implémentation des classes
`HeatExchanger`, `HXSide`, `Wall`, modèles ε-NTU, etc.). Les modules de
corrélations ε-NTU contiennent des stubs qui seront remplacés par les formules
exactes.
